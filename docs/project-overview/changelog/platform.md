---
description: Be sure to not miss out on new features and improvements!
---

# Platform

This is the changelog for Airbyte Platform. For our connector changelog, please visit our [Connector Changelog](connectors.md) page.

## [07-1-2021 - 0.27.0](https://github.com/airbytehq/airbyte/releases/tag/v0.27.0-alpha)
* Airbyte now automatically upgrades on server startup!
  * Airbyte will check whether your `.env` Airbyte version is compatible with the Airbyte version in the database and upgrade accordingly.
* When running Airbyte on K8s logs will automatically be stored in a Minio bucket unless configured otherwise.
* CDC for MySQL now handles decimal types correctly.

## [06-21-2021 - 0.26.2](https://github.com/airbytehq/airbyte/releases/tag/v0.26.2-alpha)

* First-Class Kubernetes support!

## [06-16-2021 - 0.26.0](https://github.com/airbytehq/airbyte/releases/tag/v0.26.0-alpha)

* Custom dbt transformations! 
* You can now configure your destination namespace at the table level when setting up a connection!  
* Migrate basic normalization settings to the sync operations.

## [06-09-2021 - 0.24.8 / 0.25.0](https://github.com/airbytehq/airbyte/releases/tag/v0.24.8-alpha)

* Bugfix: Handle TINYINT(1) and BOOLEAN correctly and fix target file comparison for MySQL CDC.
* Bugfix: Updating the source/destination name in the UI now works as intended.

## [06-04-2021 - 0.24.7](https://github.com/airbytehq/airbyte/releases/tag/v0.24.7-alpha)

* Bugfix: Ensure that logs from threads created by replication workers are added to the log file.

## [06-03-2021 - 0.24.5](https://github.com/airbytehq/airbyte/releases/tag/v0.24.5-alpha)

* Remove hash from table names when it's not necessary for normalization outputs.

## [06-03-2021 - 0.24.4](https://github.com/airbytehq/airbyte/releases/tag/v0.24.4-alpha)

* PythonCDK: change minimum Python version to 3.7.0

## [05-28-2021 - 0.24.3](https://github.com/airbytehq/airbyte/releases/tag/v0.24.3-alpha)

* Minor fixes to documentation
* Reliability updates in preparation for custom transformations  
* Limit Docker log size to 500 MB ([#3702](https://github.com/airbytehq/airbyte/pull/3702))

## [05-26-2021 - 0.24.2](https://github.com/airbytehq/airbyte/releases/tag/v0.24.2-alpha)

* Fix for file names being too long in Windows deployments ([#3625](https://github.com/airbytehq/airbyte/pull/3625))
* Allow users to access the API and WebApp from the same port ([#3603](https://github.com/airbytehq/airbyte/pull/3603))

## [05-25-2021 - 0.24.1](https://github.com/airbytehq/airbyte/releases/tag/v0.24.1-alpha)

* **Checkpointing for incremental syncs** that will now continue where they left off even if they fail! ([#3290](https://github.com/airbytehq/airbyte/pull/3290))

## [05-25-2021 - 0.24.0](https://github.com/airbytehq/airbyte/releases/tag/v0.24.0-alpha)

* Avoid dbt runtime exception "maximum recursion depth exceeded" in ephemeral materialization ([#3470](https://github.com/airbytehq/airbyte/pull/3470))

## [05-18-2021 - 0.23.0](https://github.com/airbytehq/airbyte/releases/tag/v0.23.0-alpha)

* Documentation to deploy locally on Windows is now available ([#3425](https://github.com/airbytehq/airbyte/pull/3425))
* Connector icons are now displayed in the UI
* Restart core containers if they fail automatically ([#3423](https://github.com/airbytehq/airbyte/pull/3423))
* Progress on supporting custom transformation using dbt. More updates on this soon!

## [05-11-2021 - 0.22.3](https://github.com/airbytehq/airbyte/releases/tag/v0.22.3-alpha)

* Bump K8s deployment version to latest stable version, thanks to [Coetzee van Staden](https://github.com/coetzeevs)
* Added tutorial to deploy Airbyte on Azure VM \([\#3171](https://github.com/airbytehq/airbyte/pull/3171)\), thanks to [geekwhocodes](https://github.com/geekwhocodes)
* Progress on checkpointing to support rate limits better
* Upgrade normalization to use dbt from docker images \([\#3186](https://github.com/airbytehq/airbyte/pull/3186)\)

## [05-04-2021 - 0.22.2](https://github.com/airbytehq/airbyte/releases/tag/v0.22.2-alpha)

* Split replication and normalization into separate temporal activities \([\#3136](https://github.com/airbytehq/airbyte/pull/3136)\)
* Fix normalization Nesting bug \([\#3110](https://github.com/airbytehq/airbyte/pull/3110)\)

## [04-27-2021 - 0.22.0](https://github.com/airbytehq/airbyte/releases/tag/v0.22.0-alpha)

* **Replace timeout for sources** \([\#3031](https://github.com/airbytehq/airbyte/pull/2851)\)
* Fix UI issue where tables with the same name are selected together \([\#3032](https://github.com/airbytehq/airbyte/pull/2851)\)
* Fix feed handling when feeds are unavailable \([\#2964](https://github.com/airbytehq/airbyte/pull/2851)\)
* Export whitelisted tables \([\#3055](https://github.com/airbytehq/airbyte/pull/2851)\)
* Create a contributor bootstrap script \(\#3028\) \([\#3054](https://github.com/airbytehq/airbyte/pull/2851)\), thanks to [nclsbayona](https://github.com/nclsbayona)

## [04-20-2021 - 0.21.0](https://github.com/airbytehq/airbyte/releases/tag/v0.21.0-alpha)

* **Namespace support**: supported source-destination pairs will now sync data into the same namespace as the source \(\#2862\)
* Add **“Refresh Schema”** button \([\#2943](https://github.com/airbytehq/airbyte/pull/2943)\)
* In the Settings, you can now **add a webhook to get notified when a sync fails**
* Add destinationSyncModes to connection form
* Add tooltips for connection status icons

## [04-12-2021 - 0.20.0](https://github.com/airbytehq/airbyte/releases/tag/v0.20.0-alpha)

* **Change Data Capture \(CDC\)** is now supported for Postgres, thanks to [@jrhizor](https://github.com/jrhizor) and [@cgardens](https://github.com/cgardens). We will now expand it to MySQL and MSSQL in the coming weeks.
* When displaying the schema for a source, you can now search for table names, thanks to [@jamakase](https://github.com/jamakase)
* Better feedback UX when manually triggering a sync with “Sync now”

## [04-07-2021 - 0.19.0](https://github.com/airbytehq/airbyte/releases/tag/v0.19.0-alpha)

* New **Connections** page where you can see the list of all your connections and their statuses. 
* New **Settings** page to update your preferences.
* Bugfix where very large schemas caused schema discovery to fail.

## [03-29-2021 - 0.18.1](https://github.com/airbytehq/airbyte/releases/tag/v0.18.1-alpha)

* Surface the **health of each connection** so that a user can spot any problems at a glance. 
* Added support for deduplicating records in the destination using a primary key using incremental dedupe -  
* A source’s extraction mode \(incremental, full refresh\) is now decoupled from the destination’s write mode -- so you can repeatedly append full refreshes to get repeated snapshots of data in your source.
* New **Upgrade all** button in Admin to upgrade all your connectors at once 
* New **Cancel** job button in Connections Status page when a sync job is running, so you can stop never-ending processes.

## [03-22-2021 - 0.17.2](https://github.com/airbytehq/airbyte/releases/tag/v0.17.2-alpha)

* Improved the speed of get spec, check connection, and discover schema by migrating to the Temporal workflow engine.
* Exposed cancellation for sync jobs in the API \(will be exposed in the UI in the next week!\).
* Bug fix: Fix issue where migration app was OOMing.

## [03-15-2021 - 0.17.1](https://github.com/airbytehq/airbyte/releases/tag/v0.17.1-alpha)

* **Creating and deleting multiple workspaces** is now supported via the API. Thanks to [@Samuel Gordalina](https://github.com/gordalina) for contributing this feature!
* Normalization now supports numeric types with precision greater than 32 bits
* Normalization now supports union data types
* Support longform text inputs in the UI for cases where you need to preserve formatting on connector inputs like .pem keys
* Expose the latest available connector versions in the API
* Airflow: published a new [tutorial](https://docs.airbyte.io/tutorials/using-the-airflow-airbyte-operator) for how to use the Airbyte operator. Thanks [@Marcos Marx](https://github.com/marcosmarxm) for writing the tutorial! 
* Connector Contributions: All connectors now describe how to contribute to them without having to touch Airbyte’s monorepo build system -- just work on the connector in your favorite dev setup!

## [03-08-2021 - 0.17](https://github.com/airbytehq/airbyte/releases/tag/v0.17.0-alpha)

* **Integration with Airflow** is here. Thanks to @Marcos Marx, you can now run Airbyte jobs from Airflow directly. A tutorial is on the way and should be coming this week!
* Add a prefix for tables, so that tables with the same name don't clobber each other in the destination

## [03-01-2021 - 0.16](https://github.com/airbytehq/airbyte/milestone/22?closed=1)

* We made some progress to address **nested tables in our normalization.**

  Previously, basic normalization would output nested tables as-is and append a number for duplicate tables. For example, Stripe’s nested address fields go from:

  ```text
  Address
  address_1
  ```

  To

  ```text
  Charges_source_owner_755_address
  customers_shipping_c70_address
  ```

  After the change, the parent tables are combined with the name of the nested table to show where the nested table originated. **This is a breaking change for the consumers of nested tables. Consumers will need to update to point at the new tables.**

## [02-19-2021 - 0.15](https://github.com/airbytehq/airbyte/milestone/22?closed=1)

* We now handle nested tables with the normalization steps. Check out the video below to see how it works. 

{% embed url="https://youtu.be/I4fngMnkJzY" caption="" %}

## [02-12-2021 - 0.14](https://github.com/airbytehq/airbyte/milestone/21?closed=1)

* Front-end changes:
  * Display Airbyte's version number
  * Describe schemas using JsonSchema
  * Better feedback on buttons

## [Beta launch - 0.13](https://github.com/airbytehq/airbyte/milestone/15?closed=1) - Released 02/02/2021

* Add connector build status dashboard
* Support Schema Changes in Sources
* Support Import / Export of Airbyte Data in the Admin section of the UI
* Bug fixes:
  * If Airbyte is closed during a sync the running job is not marked as failed
  * Airbyte should fail when instance version doesn't match data version
  * Upgrade Airbyte Version without losing existing configuration / data

## [0.12-alpha](https://github.com/airbytehq/airbyte/milestone/14?closed=1) - Released 01/20/2021

* Ability to skip onboarding
* Miscellaneous bug fixes:
  * A long discovery request causes a timeout in the UI type/bug
  * Out of Memory when replicating large table from MySQL

## 0.11.2-alpha - Released 01/18/2021

* Increase timeout for long running catalog discovery operations from 3 minutes to 30 minutes to avoid prematurely failing long-running operations 

## 0.11.1-alpha - Released 01/17/2021

### Bugfixes

* Writing boolean columns to Redshift destination now works correctly 

## [0.11.0-alpha](https://github.com/airbytehq/airbyte/milestone/12?closed=1) - Delivered 01/14/2021

### New features

* Allow skipping the onboarding flow in the UI
* Add the ability to reset a connection's schema when the underlying data source schema changes

### Bugfixes

* Fix UI race condition which showed config for the wrong connector when rapidly choosing between different connector 
* Fix a bug in MSSQL and Redshift source connectors where custom SQL types weren't being handled correctly. [Pull request](https://github.com/airbytehq/airbyte/pull/1576)
* Support incremental sync for Salesforce, Slack, and Braintree sources
* Gracefully handle invalid nuemric values \(e.g NaN or Infinity\) in MySQL, MSSQL, and Postgtres DB sources
* Fix flashing red sources/destinations fields after success submit
* Fix a bug which caused getting a connector's specification to hang indefinitely if the connector docker image failed to download

### New connectors

* Tempo
* Appstore

## [0.10.0](https://github.com/airbytehq/airbyte/milestone/12?closed=1) - delivered on 01/04/2021

* You can now **deploy Airbyte on** [**Kuberbetes**](https://docs.airbyte.io/deploying-airbyte/on-kubernetes) _\*\*_\(alpha version\)
* **Support incremental sync** for Mixpanel and Hubspot sources
* **Fixes on connectors:**
  * Fixed a bug in the GitHub connector where the connector didn’t verify the provided API token was granted the correct permissions
  * Fixed a bug in the Google Sheets connector where rate limits were not always respected
  * Alpha version of Facebook marketing API v9. This connector is a native Airbyte connector \(current is Singer based\).
* **New source:** Plaid \(contributed by [@tgiardina](https://github.com/tgiardina) - thanks Thomas!\)

## [0.9.0](https://github.com/airbytehq/airbyte/milestone/11?closed=1) - delivered on 12/23/2020

* **New chat app from the web app** so you can directly chat with the team for any issues you run into
* **Debugging** has been made easier in the UI, with checks, discover logs, and sync download logs
* Support of **Kubernetes in local**. GKE will come at the next release.
* **New source:** Looker _\*\*_

## [0.8.0](https://github.com/airbytehq/airbyte/milestone/10?closed=1) - delivered on 12/17/2020

* **Incremental - Append"**
  * We now allow sources to replicate only new or modified data. This enables to avoid re-fetching data that you have already replicated from a source.
  * The delta from a sync will be _appended_ to the existing data in the data warehouse.
  * Here are [all the details of this feature](../../understanding-airbyte/connections/incremental-append.md).
  * It has been released for 15 connectors, including Postgres, MySQL, Intercom, Zendesk, Stripe, Twilio, Marketo, Shopify, GitHub, and all the destination connectors. We will expand it to all the connectors in the next couple of weeks.
* **Other features:**
  * Improve interface for writing python sources \(should make writing new python sources easier and clearer\).
  * Add support for running Standard Source Tests with files \(making them easy to run for any language a source is written in\)
  * Add ability to reset data for a connection.
* **Bug fixes:**
  * Update version of test containers we use to avoid pull issues while running tests.
  * Fix issue where jobs were not sorted by created at in connection detail view.
* **New sources:** Intercom, Mixpanel, Jira Cloud, Zoom, Drift, Microsoft Teams

## [0.7.0](https://github.com/airbytehq/airbyte/milestone/8?closed=1) - delivered on 12/07/2020

* **New destination:** our own **Redshift** warehouse connector. You can also use this connector for Panoply.
* **New sources**: 8 additional source connectors including Recurly, Twilio, Freshdesk. Greenhouse, Redshift \(source\), Braintree, Slack, Zendesk Support
* Bug fixes

## [0.6.0](https://github.com/airbytehq/airbyte/milestone/6?closed=1) - delivered on 11/23/2020

* Support **multiple destinations**
* **New source:** Sendgrid
* Support **basic normalization**
* Bug fixes

## [0.5.0](https://github.com/airbytehq/airbyte/milestone/5?closed=1) - delivered on 11/18/2020

* **New sources:** 10 additional source connectors, including Files \(CSV, HTML, JSON...\), Shopify, MSSQL, Mailchimp

## [0.4.0](https://github.com/airbytehq/airbyte/milestone/4?closed=1) - delivered on 11/04/2020

Here is what we are working on right now:

* **New destination**: our own **Snowflake** warehouse connector
* **New sources:** Facebook Ads, Google Ads.

## [0.3.0](https://github.com/airbytehq/airbyte/milestone/3?closed=1) - delivered on 10/30/2020

* **New sources:** Salesforce, GitHub, Google Sheets, Google Analytics, Hubspot, Rest APIs, and MySQL
* Integration test suite for sources
* Improve build speed

## [0.2.0](https://github.com/airbytehq/airbyte/milestone/2?closed=1) - delivered on 10/21/2020

* **a new Admin section** to enable users to add their own connectors, in addition to upgrading the ones they currently use
* improve the developer experience \(DX\) for **contributing new connectors** with additional documentation and a connector protocol
* our own **BigQuery** warehouse connector
* our own **Postgres** warehouse connector
* simplify the process of supporting new Singer taps, ideally make it a 1-day process

## [0.1.0](https://github.com/airbytehq/airbyte/milestone/1?closed=1) - delivered on 09/23/2020

This is our very first release after 2 months of work.

* **New sources:** Stripe, Postgres
* **New destinations:** BigQuery, Postgres
* **Only one destination**: we only support one destination in that 1st release, but you will soon be able to add as many as you need.
* **Logs & monitoring**: you can now see your detailed logs
* **Scheduler:** you now have 10 different frequency options for your recurring syncs
* **Deployment:** you can now deploy Airbyte via a simple Docker image, or directly on AWS and GCP
* **New website**: this is the day we launch our website - airbyte.io. Let us know what you think
* **New documentation:** this is the 1st day for our documentation too
* **New blog:** we published a few articles on our startup journey, but also about our vision to making data integrations a commodity.

Stay tuned, we will have new sources and destinations very soon! Don't hesitate to subscribe to our [newsletter](https://airbyte.io/#subscribe-newsletter) to receive our product updates and community news.

