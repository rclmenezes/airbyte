#
# MIT License
#
# Copyright (c) 2020 Airbyte
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import json
from abc import ABC, abstractmethod
from typing import Any, Iterable, List, Mapping, MutableMapping, Optional, Tuple
from source_square.utils import separate_items_by_count

import pendulum
import requests
from airbyte_cdk.models import SyncMode
from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.sources.streams import Stream
from airbyte_cdk.sources.streams.http import HttpStream
from airbyte_cdk.sources.streams.http.auth import TokenAuthenticator


class SquareStream(HttpStream, ABC):
    def __init__(self, is_sandbox: bool, api_version: str, start_date: str, include_deleted_objects: bool, **kwargs):
        super().__init__(**kwargs)
        self.is_sandbox = is_sandbox
        self.api_version = api_version
        # Converting users ISO 8601 format (YYYY-MM-DD) to RFC 3339 (2021-06-14T13:47:56.799Z)
        # Because this standard is used by square in 'updated_at' records field
        self.start_date = pendulum.parse(start_date).to_rfc3339_string()
        self.include_deleted_objects = include_deleted_objects

    data_field = None
    primary_key = "id"
    items_per_page_limit = 100

    @property
    def url_base(self) -> str:
        return "https://connect.squareup{}.com/v2/".format("sandbox" if self.is_sandbox else "")

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        next_page_cursor = response.json().get("cursor", False)
        if next_page_cursor:
            return {"cursor": next_page_cursor}

    def request_headers(
            self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, Any] = None,
            next_page_token: Mapping[str, Any] = None
    ) -> Mapping[str, Any]:
        return {"Square-Version": self.api_version, "Content-Type": "application/json"}

    def parse_response(self, response: requests.Response, **kwargs) -> Iterable[Mapping]:
        json_response = response.json()
        records = json_response.get(self.data_field, []) if self.data_field is not None else json_response
        yield from records

    def _send_request(self, request: requests.PreparedRequest) -> requests.Response:
        try:
            return super()._send_request(request)
        except requests.exceptions.HTTPError as e:
            if e.response.content:
                content = json.loads(e.response.content.decode())
                if content and "errors" in content:
                    square_exception = SquareException(e.response.status_code, content["errors"])
                    self.logger.error(str(square_exception))
                    exit(1)
            else:
                raise e


class SquareException(Exception):
    """ Just for formatting the exception as Square"""

    def __init__(self, status_code, errors):
        self.status_code = status_code
        self.errors = errors

    def __str__(self):
        return f"Code: {self.status_code}, Detail: {self.errors}"


class SquareStreamPageParam(SquareStream, ABC):
    def request_params(
            self,
            stream_state: Mapping[str, Any],
            stream_slice: Mapping[str, Any] = None,
            next_page_token: Mapping[str, Any] = None
    ) -> MutableMapping[str, Any]:
        return {'cursor': next_page_token['cursor']} if next_page_token else {}


class SquareStreamPageJson(SquareStream, ABC):
    def request_body_json(
            self,
            stream_state: Mapping[str, Any],
            stream_slice: Mapping[str, Any] = None,
            next_page_token: Mapping[str, Any] = None
    ) -> Optional[Mapping]:
        return {'cursor': next_page_token['cursor']} if next_page_token else {}


class SquareStreamPageJsonAndLimit(SquareStreamPageJson, ABC):
    def request_body_json(
            self,
            stream_state: Mapping[str, Any],
            stream_slice: Mapping[str, Any] = None,
            next_page_token: Mapping[str, Any] = None
    ) -> Optional[Mapping]:
        json_payload = {'limit': self.items_per_page_limit}
        if next_page_token:
            json_payload.update(next_page_token)

        return json_payload


class SquareCatalogObjectsStream(SquareStreamPageJson):
    data_field = "objects"
    http_method = "POST"
    items_per_page_limit = 1000

    def path(self, **kwargs) -> str:
        return "catalog/search"

    def request_body_json(
            self,
            stream_state: Mapping[str, Any],
            stream_slice: Mapping[str, Any] = None,
            next_page_token: Mapping[str, Any] = None) -> Optional[Mapping]:
        json_payload = super().request_body_json(stream_state, stream_slice, next_page_token)

        if self.path() == "catalog/search":
            json_payload["include_deleted_objects"] = self.include_deleted_objects
            json_payload["include_related_objects"] = False
            json_payload["limit"] = self.items_per_page_limit

        return json_payload


class IncrementalSquareGenericStream(SquareStream, ABC):
    def get_updated_state(
            self,
            current_stream_state: MutableMapping[str, Any],
            latest_record: Mapping[str, Any]
    ) -> Mapping[str, Any]:
        if current_stream_state is not None and self.cursor_field in current_stream_state:
            return {self.cursor_field: max(current_stream_state[self.cursor_field], latest_record[self.cursor_field])}
        else:
            return {self.cursor_field: self.start_date}


class IncrementalSquareCatalogObjectsStream(SquareCatalogObjectsStream, IncrementalSquareGenericStream, ABC):
    @property
    @abstractmethod
    def object_type(self):
        """Object type property"""

    state_checkpoint_interval = SquareCatalogObjectsStream.items_per_page_limit

    cursor_field = "updated_at"

    def request_body_json(self, stream_state: Mapping[str, Any], **kwargs) -> Optional[Mapping]:
        json_payload = super().request_body_json(stream_state, **kwargs)

        if stream_state:
            json_payload["begin_time"] = stream_state[self.cursor_field]

        json_payload["object_types"] = [self.object_type]
        return json_payload


class IncrementalSquareStream(IncrementalSquareGenericStream, SquareStreamPageParam, ABC):
    state_checkpoint_interval = SquareStream.items_per_page_limit

    cursor_field = "created_at"

    def request_params(
            self,
            stream_state: Mapping[str, Any],
            stream_slice: Mapping[str, Any] = None,
            next_page_token: Mapping[str, Any] = None,
    ) -> MutableMapping[str, Any]:
        params_payload = super().request_params(stream_state, stream_slice, next_page_token)

        if stream_state:
            params_payload["begin_time"] = stream_state[self.cursor_field]

        params_payload["limit"] = self.items_per_page_limit

        return params_payload


class Items(IncrementalSquareCatalogObjectsStream):
    """Docs: https://developer.squareup.com/explorer/square/catalog-api/search-catalog-objects
    with object_types = ITEM"""
    object_type = "ITEM"


class Categories(IncrementalSquareCatalogObjectsStream):
    """Docs: https://developer.squareup.com/explorer/square/catalog-api/search-catalog-objects
    with object_types = CATEGORY"""
    object_type = "CATEGORY"


class Discounts(IncrementalSquareCatalogObjectsStream):
    """Docs: https://developer.squareup.com/explorer/square/catalog-api/search-catalog-objects
    with object_types = DISCOUNT"""
    object_type = "DISCOUNT"


class Taxes(IncrementalSquareCatalogObjectsStream):
    """Docs: https://developer.squareup.com/explorer/square/catalog-api/search-catalog-objects
    with object_types = TAX"""
    object_type = "TAX"


class ModifierList(IncrementalSquareCatalogObjectsStream):
    """Docs: https://developer.squareup.com/explorer/square/catalog-api/search-catalog-objects
    with object_types = MODIFIER_LIST"""
    object_type = "MODIFIER_LIST"


class Refunds(IncrementalSquareStream):
    """ Docs: https://developer.squareup.com/reference/square_2021-06-16/refunds-api/list-payment-refunds """

    data_field = "refunds"

    def path(self, **kwargs) -> str:
        return "refunds"

    def request_params(self, **kwargs) -> MutableMapping[str, Any]:
        params_payload = super().request_params(**kwargs)
        params_payload["sort_order"] = "ASC"

        return params_payload


class Payments(IncrementalSquareStream):
    """ Docs: https://developer.squareup.com/reference/square_2021-06-16/payments-api/list-payments """

    data_field = "payments"

    def path(self, **kwargs) -> str:
        return "payments"

    def request_params(self, **kwargs) -> MutableMapping[str, Any]:
        params_payload = super().request_params(**kwargs)
        params_payload["sort_order"] = "ASC"

        return params_payload


class Locations(SquareStream):
    """ Docs: https://developer.squareup.com/explorer/square/locations-api/list-locations """

    data_field = "locations"

    def path(
            self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None,
            next_page_token: Mapping[str, Any] = None
    ) -> str:
        return "locations"


class Shifts(SquareStreamPageJsonAndLimit):
    """ Docs: https://developer.squareup.com/reference/square/labor-api/search-shifts """

    data_field = "shifts"
    http_method = "POST"
    items_per_page_limit = 200

    def path(self, **kwargs) -> str:
        return "labor/shifts/search"


class TeamMembers(SquareStreamPageJsonAndLimit):
    """ Docs: https://developer.squareup.com/reference/square/team-api/search-team-members """

    data_field = "team_members"
    http_method = "POST"

    def path(
            self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None,
            next_page_token: Mapping[str, Any] = None
    ) -> str:
        return "team-members/search"


class TeamMemberWages(SquareStreamPageParam):
    """ Docs: https://developer.squareup.com/reference/square_2021-06-16/labor-api/list-team-member-wages """

    data_field = "team_member_wages"
    items_per_page_limit = 200

    def path(self, **kwargs) -> str:
        return "labor/team-member-wages"

    def request_params(self, **kwargs) -> MutableMapping[str, Any]:
        params_payload = super().request_params(**kwargs)
        params_payload = params_payload or {}

        params_payload["limit"] = self.items_per_page_limit
        return params_payload


class Customers(SquareStreamPageParam):
    """ Docs: https://developer.squareup.com/reference/square_2021-06-16/customers-api/list-customers """

    data_field = "customers"

    def path(self, **kwargs) -> str:
        return "customers"

    def request_params(self, **kwargs) -> MutableMapping[str, Any]:
        params_payload = super().request_params(**kwargs)
        params_payload = params_payload or {}

        params_payload["sort_order"] = "ASC"
        params_payload["sort_field"] = "CREATED_AT"
        return params_payload


class Orders(SquareStreamPageJson):
    """ Docs: https://developer.squareup.com/reference/square/orders-api/search-orders """

    data_field = "orders"
    http_method = "POST"
    items_per_page_limit = 500

    def path(self, **kwargs) -> str:
        return "orders/search"

    def request_body_json(self, **kwargs) -> Optional[Mapping]:
        json_payload = super().request_body_json(**kwargs)
        json_payload = json_payload or {}

        locations_stream = Locations(
            authenticator=self.authenticator,
            is_sandbox=self.is_sandbox,
            api_version=self.api_version,
            start_date=self.start_date,
            include_deleted_objects=self.include_deleted_objects
        )
        locations_records = locations_stream.read_records(sync_mode=SyncMode.full_refresh)
        location_ids = [location["id"] for location in locations_records]

        if location_ids:
            json_payload["location_ids"] = location_ids

        json_payload["limit"] = self.items_per_page_limit
        return json_payload

    def read_records(
            self,
            sync_mode: SyncMode,
            cursor_field: List[str] = None,
            stream_slice: Mapping[str, Any] = None,
            stream_state: Mapping[str, Any] = None,
    ) -> Iterable[Mapping[str, Any]]:
        json_payload = self.request_body_json(stream_state=stream_state, stream_slice=stream_slice,
                                              next_page_token=None)
        if 'location_ids' not in json_payload:
            self.logger.info('No location records found.')
            yield from []

        # There is a restriction in the documentation where only 10 locations can be send at one request
        # https://developer.squareup.com/reference/square/orders-api/search-orders#request__property-location_ids
        location_ids = json_payload['location_ids']
        separated_locations = separate_items_by_count(location_ids, 10)

        stream_state = stream_state or {}
        pagination_complete = False

        for locations in separated_locations:
            json_payload['location_ids'] = locations
            next_page_token = None
            while not pagination_complete:
                request_headers = self.request_headers(stream_state=stream_state, stream_slice=stream_slice,
                                                       next_page_token=next_page_token)
                request = self._create_prepared_request(
                    path=self.path(stream_state=stream_state, stream_slice=stream_slice,
                                   next_page_token=next_page_token),
                    headers=dict(request_headers, **self.authenticator.get_auth_header()),
                    params=self.request_params(stream_state=stream_state, stream_slice=stream_slice,
                                               next_page_token=next_page_token),
                    json=json_payload,
                )

                response = self._send_request(request)
                yield from self.parse_response(response, stream_state=stream_state, stream_slice=stream_slice)

                next_page_token = self.next_page_token(response)
                if not next_page_token:
                    pagination_complete = True

            # Always return an empty generator just in case no records were ever yielded
            yield from []


class SourceSquare(AbstractSource):
    api_version = "2021-06-16"  # Latest Stable Release

    def check_connection(self, logger, config) -> Tuple[bool, any]:

        headers = {
            "Square-Version": self.api_version,
            "Authorization": "Bearer {}".format(config["api_key"]),
            "Content-Type": "application/json",
        }
        url = "https://connect.squareup{}.com/v2/catalog/info".format("sandbox" if config["is_sandbox"] else "")

        try:
            session = requests.get(url, headers=headers)
            session.raise_for_status()
            return True, None
        except requests.exceptions.RequestException as e:
            if e.response.status_code == 401:
                return False, "Unauthorized. Check your credentials"

            return False, e

    def streams(self, config: Mapping[str, Any]) -> List[Stream]:

        auth = TokenAuthenticator(token=config["api_key"])
        args = {
            "authenticator": auth,
            "is_sandbox": config["is_sandbox"],
            "api_version": self.api_version,
            "start_date": config["start_date"],
            "include_deleted_objects": config["include_deleted_objects"],
        }
        return [
            Items(**args),
            Categories(**args),
            Discounts(**args),
            Taxes(**args),
            Locations(**args),
            TeamMembers(**args),
            TeamMemberWages(**args),
            Refunds(**args),
            Payments(**args),
            Customers(**args),
            ModifierList(**args),
            Shifts(**args),
            Orders(**args),
        ]
