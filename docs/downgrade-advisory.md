# Downgrade Advisory Tool

`tools/downgrade-advisory.py` converts a GitHub security advisory into a public
bug report. It fetches the advisory by GHSA ID, scrubs the reporter identity and
other sensitive metadata, files a public issue that preserves the technical
description, and closes the original advisory with a link to the new issue.

Use this when a maintainer decides a report does not warrant a CVE and should
instead be tracked in the open as a regular bug.

## Prerequisites

The tool needs the `gh` CLI authenticated with a token that has the `repo`
scope. The `security_events` scope is not required, since it governs code
scanning and secret scanning rather than repository advisories.

You do not need to be a repository administrator or security manager. Being a
collaborator on the advisory is enough: GitHub grants advisory collaborators
both read and update access, which is all the tool uses to fetch the advisory
and then close it.

## Usage

```bash
python3 tools/downgrade-advisory.py GHSA-xxxx-xxxx-xxxx            # preview
python3 tools/downgrade-advisory.py GHSA-xxxx-xxxx-xxxx --apply    # create issue
```

The positional argument may be a bare GHSA ID or a full advisory URL such as
`https://github.com/<owner>/<repo>/security/advisories/GHSA-xxxx-xxxx-xxxx`. When
a URL is given, the repository it points at is used as the source.

## Flags

| Flag | Description |
| ---- | ----------- |
| `--apply` | Create the issue and close the advisory. Without it the script prints a dry-run preview. |
| `--repo OWNER/REPO` | Source repository. Defaults to the `$REPO` environment variable, then to `open-telemetry/opentelemetry-collector-contrib`. |
| `--target-repo OWNER/REPO` | Repository to create the issue in. Defaults to the source repository. |
| `--label LABEL` | Label to add to the issue, repeatable. Defaults to `bug`. |
