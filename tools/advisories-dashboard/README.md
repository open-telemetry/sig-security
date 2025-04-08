# GitHub Security Advisories Dashboard

The SIG Security developed an automation to make it easier for GC and TC members
to visualize the security advisories across all OpenTelemetry repositories.

The script in the repository `open-telemetry-private/private-incident-tracking`,
builds a CSV file that is committed to the same repository on a different branch
(`data-source`). The CSV is used as a data source in a Grafana dashboard, and
accessible to SIG Security, OTel GC, and OTel TC people who requested access.

The script is triggered either daily or manually by a GitHub Action.

## Private repository

https://github.com/open-telemetry-private/private-incident-tracking

The following people have access to this repository:

* @jpkrohling
* @ms-jcorley
* @reyang

SIG Security, OTel GC, and OTel TC members are welcome to request access. To do
so, please open an issue on this repository.

## Grafana dashboard

https://otelsigsecurity.grafana.net

The following people have access to this dashboard:

* @arminru
* @jack-berg
* @jpkrohling
* @jsuereth
* @lmolkova
* @tigrannajaryan

SIG Security, OTel GC, and OTel TC members are welcome to request access. To do
so, please open an issue on this repository.
