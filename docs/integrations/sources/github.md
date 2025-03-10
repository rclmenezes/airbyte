# GitHub

## Overview

The GitHub source supports both Full Refresh and Incremental syncs. You can choose if this connector will copy only the new or updated data, or all rows in the tables and columns you set up for replication, every time a sync is run.

This Github source wraps the [Singer Github Tap](https://github.com/singer-io/tap-github).

### Output schema

This connector outputs the following full refresh streams:

* [Assignees](https://docs.github.com/en/rest/reference/issues#list-assignees)
* [Reviews](https://docs.github.com/en/rest/reference/pulls#list-reviews-for-a-pull-request)
* [Collaborators](https://docs.github.com/en/rest/reference/repos#list-repository-collaborators)
* [Teams](https://docs.github.com/en/rest/reference/teams#list-teams)
* [Issue labels](https://docs.github.com/en/free-pro-team@latest/rest/reference/issues#list-labels-for-a-repository)

This connector outputs the following incremental streams:

* [Comments](https://docs.github.com/en/rest/reference/issues#list-issue-comments-for-a-repository)
* [Commits](https://docs.github.com/en/rest/reference/issues#list-issue-comments-for-a-repository)
* [Issues](https://docs.github.com/en/rest/reference/issues#list-repository-issues)
* [Commit comments](https://docs.github.com/en/rest/reference/repos#list-commit-comments-for-a-repository)
* [Events](https://docs.github.com/en/rest/reference/activity#list-repository-events)
* [Issue events](https://docs.github.com/en/rest/reference/issues#list-issue-events-for-a-repository)
* [Issue milestones](https://docs.github.com/en/rest/reference/issues#list-milestones)
* [Projects](https://docs.github.com/en/rest/reference/projects#list-repository-projects)
* [Pull requests](https://docs.github.com/en/rest/reference/pulls#list-pull-requests)
* [Releases](https://docs.github.com/en/rest/reference/repos#list-releases)
* [Stargazers](https://docs.github.com/en/rest/reference/activity#list-stargazers)

**Note:** Only 3 streams from above 11 incremental streams (`comments`, `commits` and `issues`) are pure incremental 
meaning that they:
- read only new records;
- output only new records.

Other 8 incremental streams are also incremental but with one difference, they:
- read all records;
- output only new records.

Please, consider this behaviour when using those 8 incremental streams because it may affect you API call limits. 

### Features

| Feature | Supported? |
| :--- | :--- |
| Full Refresh Sync | Yes |
| Incremental - Append Sync | Yes |
| Replicate Incremental Deletes | Coming soon |
| SSL connection | Yes |
| Namespaces | No |

### Performance considerations

The Github connector should not run into Github API limitations under normal usage. Please [create an issue](https://github.com/airbytehq/airbyte/issues) if you see any rate limit issues that are not automatically retried successfully.

## Getting started

### Requirements

* Github Account;
* `access_token` - Github Personal Access Token wih the necessary permissions \(described below\);
* `repository` - GitHub repository which looks like `<owner>/<repo>`;
* `start_date` - start date for 3 incremental streams: `comments`, `commits` and `issues`.

### Setup guide

Log into Github and then generate a [personal access token](https://github.com/settings/tokens).

Your token should have at least the `repo` scope. Depending on which streams you want to sync, the user generating the token needs more permissions:

* For syncing Collaborators, the user which generates the personal access token must be a collaborator. To become a collaborator, they must be invited by an owner. If there are no collaborators, no records will be synced. Read more about access permissions [here](https://docs.github.com/en/free-pro-team@latest/github/getting-started-with-github/access-permissions-on-github).
* Syncing [Teams](https://docs.github.com/en/free-pro-team@latest/github/setting-up-and-managing-organizations-and-teams/about-teams) is only available to authenticated members of a team's [organization](https://docs.github.com/en/free-pro-team@latest/rest/reference/orgs). [Personal user accounts](https://docs.github.com/en/free-pro-team@latest/github/getting-started-with-github/types-of-github-accounts) and repositories belonging to them don't have access to Teams features. In this case no records will be synced.
* To sync the Projects stream, the repository must have the Projects feature enabled.

