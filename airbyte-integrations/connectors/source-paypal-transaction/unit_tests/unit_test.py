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

from datetime import datetime, timedelta

from airbyte_cdk.sources.streams.http.auth import NoAuth
from dateutil.parser import isoparse
from source_paypal_transaction.source import Balances, PaypalTransactionStream, Transactions


def test_get_field():

    record = {"a": {"b": {"c": "d"}}}
    # Test expected result - field_path is a list
    assert "d" == PaypalTransactionStream.get_field(record, field_path=["a", "b", "c"])
    # Test expected result - field_path is a string
    assert {"b": {"c": "d"}} == PaypalTransactionStream.get_field(record, field_path="a")

    # Test failures - not existing field_path
    assert None is PaypalTransactionStream.get_field(record, field_path=["a", "b", "x"])
    assert None is PaypalTransactionStream.get_field(record, field_path=["a", "x", "x"])
    assert None is PaypalTransactionStream.get_field(record, field_path=["x", "x", "x"])

    # Test failures - incorrect record structure
    record = {"a": [{"b": {"c": "d"}}]}
    assert None is PaypalTransactionStream.get_field(record, field_path=["a", "b", "c"])

    record = {"a": {"b": "c"}}
    assert None is PaypalTransactionStream.get_field(record, field_path=["a", "b", "c"])

    record = {}
    assert None is PaypalTransactionStream.get_field(record, field_path=["a", "b", "c"])


def test_update_field():
    # Test success 1
    record = {"a": {"b": {"c": "d"}}}
    PaypalTransactionStream.update_field(record, field_path=["a", "b", "c"], update=lambda x: x.upper())
    assert record == {"a": {"b": {"c": "D"}}}

    # Test success 2
    record = {"a": {"b": {"c": "d"}}}
    PaypalTransactionStream.update_field(record, field_path="a", update=lambda x: "updated")
    assert record == {"a": "updated"}

    # Test failure - incorrect field_path
    record = {"a": {"b": {"c": "d"}}}
    PaypalTransactionStream.update_field(record, field_path=["a", "b", "x"], update=lambda x: x.upper())
    assert record == {"a": {"b": {"c": "d"}}}

    # Test failure - incorrect field_path
    record = {"a": {"b": {"c": "d"}}}
    PaypalTransactionStream.update_field(record, field_path=["a", "x", "x"], update=lambda x: x.upper())
    assert record == {"a": {"b": {"c": "d"}}}


def now():
    return datetime.now().replace(microsecond=0).astimezone()


def test_transactions_stream_slices():

    start_date_init = now() - timedelta(days=2)
    t = Transactions(authenticator=NoAuth(), start_date=start_date_init)

    # if start_date > now - start_date_max then no slices
    t.start_date = now() - timedelta(**t.start_date_max) + timedelta(minutes=2)
    stream_slices = t.stream_slices(sync_mode="any")
    assert 0 == len(stream_slices)

    # start_date <= now - start_date_max
    t.start_date = now() - timedelta(**t.start_date_max)
    stream_slices = t.stream_slices(sync_mode="any")
    assert 1 == len(stream_slices)

    t.start_date = now() - timedelta(**t.start_date_max) - timedelta(hours=2)
    stream_slices = t.stream_slices(sync_mode="any")
    assert 2 == len(stream_slices)

    t.start_date = now() - timedelta(**t.start_date_max) - timedelta(days=1)
    stream_slices = t.stream_slices(sync_mode="any")
    assert 2 == len(stream_slices)

    t.start_date = now() - timedelta(**t.start_date_max) - timedelta(days=1, hours=2)
    stream_slices = t.stream_slices(sync_mode="any")
    assert 3 == len(stream_slices)

    t.start_date = now() - timedelta(**t.start_date_max) - timedelta(days=30, minutes=1)
    stream_slices = t.stream_slices(sync_mode="any")
    assert 32 == len(stream_slices)

    t.start_date = isoparse("2021-06-01T10:00:00+00:00")
    t.end_date = isoparse("2021-06-04T12:00:00+00:00")
    stream_slices = t.stream_slices(sync_mode="any")
    assert [
        {"start_date": "2021-06-01T10:00:00+00:00", "end_date": "2021-06-02T00:00:00+00:00"},
        {"start_date": "2021-06-02T00:00:00+00:00", "end_date": "2021-06-03T00:00:00+00:00"},
        {"start_date": "2021-06-03T00:00:00+00:00", "end_date": "2021-06-04T12:00:00+00:00"},
    ] == stream_slices

    stream_slices = t.stream_slices(sync_mode="any", stream_state={"date": "2021-06-02T10:00:00+00:00"})
    assert [
        {"start_date": "2021-06-02T10:00:00+00:00", "end_date": "2021-06-03T00:00:00+00:00"},
        {"start_date": "2021-06-03T00:00:00+00:00", "end_date": "2021-06-04T12:00:00+00:00"},
    ] == stream_slices

    stream_slices = t.stream_slices(sync_mode="any", stream_state={"date": "2021-06-04T10:00:00+00:00"})
    assert [] == stream_slices


def test_balances_stream_slices():

    start_date_init = now()
    b = Balances(authenticator=NoAuth(), start_date=start_date_init)
    stream_slices = b.stream_slices(sync_mode="any")
    assert 1 == len(stream_slices)

    # b.start_date = isoparse("2021-06-01T10:00:00+00:00")
    # b.end_date = isoparse("2021-06-03T12:00:00+00:00")
    # stream_slices = b.stream_slices(sync_mode="any")
    # assert [
    #     {"start_date": "2021-06-01T10:00:00+00:00"},
    #     {"start_date": "2021-06-02T10:00:00+00:00"},
    #     {"start_date": "2021-06-03T10:00:00+00:00"},
    #     {"start_date": "2021-06-03T12:00:00+00:00"},
    # ] == stream_slices

    b.start_date = now() - timedelta(minutes=1)
    b.end_date = None
    stream_slices = b.stream_slices(sync_mode="any")
    assert 2 == len(stream_slices)

    b.start_date = now() - timedelta(hours=23)
    stream_slices = b.stream_slices(sync_mode="any")
    assert 2 == len(stream_slices)

    b.start_date = now() - timedelta(days=1)
    stream_slices = b.stream_slices(sync_mode="any")
    assert 2 == len(stream_slices)

    b.start_date = now() - timedelta(days=1, minutes=1)
    stream_slices = b.stream_slices(sync_mode="any")
    assert 3 == len(stream_slices)

    b.start_date = isoparse("2021-06-01T10:00:00+00:00")
    b.end_date = isoparse("2021-06-03T12:00:00+00:00")

    stream_slices = b.stream_slices(sync_mode="any")
    assert [
        {"start_date": "2021-06-01T10:00:00+00:00"},
        {"start_date": "2021-06-02T10:00:00+00:00"},
        {"start_date": "2021-06-03T10:00:00+00:00"},
        {"start_date": "2021-06-03T12:00:00+00:00"},
    ] == stream_slices

    stream_slices = b.stream_slices(sync_mode="any", stream_state={"date": "2021-06-02T10:00:00+00:00"})
    assert [
        {"start_date": "2021-06-03T10:00:00+00:00"},
        {"start_date": "2021-06-03T12:00:00+00:00"},
    ] == stream_slices

    stream_slices = b.stream_slices(sync_mode="any", stream_state={"date": "2021-06-03T11:00:00+00:00"})
    assert [{"start_date": "2021-06-03T12:00:00+00:00"}] == stream_slices

    stream_slices = b.stream_slices(sync_mode="any", stream_state={"date": "2021-06-03T12:00:00+00:00"})
    assert [] == stream_slices
