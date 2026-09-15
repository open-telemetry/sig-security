# Repository Level Expectations

OpenTelemetry is a large project which contains multiple repositories. Each
repository has a list of
[maintainers](https://github.com/open-telemetry/community/blob/main/guides/contributor/membership.md#maintainer).
This document defines the security expectations for all the OpenTelemetry public
repositories. The target audiences are the OpenTelemetry project maintainers.

Here are the levels of expectations:

- [No Clear Expectation](#no-clear-expectation)
- [Low Expectation](#low-expectation)
- [Medium Expectation](#medium-expectation)
- [High Expectation](#high-expectation)

## No Clear Expectation

If a repository doesn't declare its security expectations, it is treated as No
Clear Expectation.

The repository owners can also explicitly declare the repository as No Clear
Expectation.

## Low Expectation

A repository is considered to meet the Low Expectation if all the conditions are
met:

- The repository maintainers (all of them) have provided their `slackMemberId`
  in the
  [`community/people.yml`](https://github.com/open-telemetry/community/blob/main/people.yml)
  file.
- The repository allows anyone who has a GitHub account to create security
  advisories.
- The repository allows anyone who has a GitHub account to create public issues.
- The repository contains a top-level `SECURITY.md` file.
- The repository's top-level `README.md` file has a security section which
  points to the `SECURITY.md` file.
- The `SECURITY.md` file has clearly explained which artifacts, services and/or
  websites are covered by the repository.
- The `SECURITY.md` file has explained how to raise security advisories and
  issues.
- The `SECURITY.md` file has explicited called out that the repository meets the
  `Low Expectation` level as defined here, with a link to this section.

## Medium Expectation

A repository is considered to meet the Medium Expectation if all the conditions
are met:

- The repository meets the [Low Expectation](#low-expectation) requirements.
- All GitHub Actions are using pinned version, an insecure version would be
  updated in less than 7 days since the patched version became available.
- The repository has onboarded to the [OpenSSF
  Scorecard](../security-dashboard.md), and the score it greater than or equal
  to `8.0`.
- The repository uses a reproducible and auditable release process.
- Security advisories and issues will be acknowledged and updated with at
  maximum 5 days delay.
- All vulnerabilities are evaluated within 7 days of detection/report.
- `Critical` level vulnerabilities are mitigated/resolved within 15 days.
- `High` level vulnerabilities are mitigated/resolved within 30 days.
- Vulnerabilities with severity level lower than `High` are mitigated/resolved
  within 60 days.
- The `SECURITY.md` file has explicited called out that the repository meets the
  `Medium Expectation` level as defined here, with a link to this section.

## High Expectation

A repository is considered to meet the High Expectation if all the conditions
are met:

- The repository meets the [Medium Expectation](#medium-expectation) requirements.
- Any individual maintainer cannot release a new version of the artifact without
  the approval of at least one other maintainer or approver.
- Security advisories and issues will be acknowledged and updated with at
  maximum 2 days delay.
- `High` level vulnerabilities are mitigated/resolved within 15 days.
- Vulnerabilities with severity level lower than `High` are mitigated/resolved
  within 30 days.
- The `SECURITY.md` file has explicited called out that the repository meets the
  `High Expectation` level as defined here, with a link to this section.
