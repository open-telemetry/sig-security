# Security Commitments Level

OpenTelemetry is a large project which contains multiple repositories. Each
repository has a list of
[maintainers](https://github.com/open-telemetry/community/blob/main/guides/contributor/membership.md#maintainer).
This document defines the security commitments for all the OpenTelemetry public
repositories. The target audiences are the OpenTelemetry project maintainers.

Here are the levels of security commitments:

- [Undeclared](#undeclared)
- [Low](#low)
- [Medium](#medium)
- [High](#high)

## Undeclared

If a repository doesn't declare its level of security commitments, it is treated
as `Undeclared`.

## Low

A repository can declare its level of security commitments as `Low` if all the
conditions are met:

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
- The `SECURITY.md` file has explicited called out that the repository provides
  the `Low` security commitments level as defined here, with a link to this
  section.

## Medium

A repository can declare its level of security commitments as `Medium` if all the
conditions are met:

- The repository meets the [Low](#low) security commitments.
- All GitHub Actions are using pinned version, an insecure version would be
  updated in less than 7 days since the patched version became available.
- The repository has onboarded to the [OpenSSF
  Scorecard](../security-dashboard.md), and the score is greater than or equal
  to `8.0`.
- The repository uses a reproducible and auditable release process.
- OIDC (OpenID Connect) is used for authentication in the publishing process,
  where available.
- Security advisories and issues will be acknowledged and updated with at
  maximum 7 days delay.
- All vulnerabilities are evaluated within 7 days of detection/report.
- `Critical` level vulnerabilities are mitigated/resolved within 30 days.
- `High` level vulnerabilities are mitigated/resolved within 45 days.
- Vulnerabilities with severity level lower than `High` are mitigated/resolved
  within 60 days.
- The `SECURITY.md` file has explicited called out that the repository provides
  the `Medium` security commitments level as defined here, with a link to this
  section.

## High

A repository can declare its level of security commitments as `High` if all the
conditions are met:

- The repository meets the [Medium](#medium) security commitments.
- Any individual maintainer cannot release a new version of the artifact without
  the approval of at least one other maintainer or approver.
- Security advisories and issues will be acknowledged and updated with at
  maximum 5 days delay.
- `Critical` level vulnerabilities are mitigated/resolved within 7 days.
- `High` level vulnerabilities are mitigated/resolved within 15 days.
- Vulnerabilities with severity level lower than `High` are mitigated/resolved
  within 30 days.
- The `SECURITY.md` file has explicited called out that the repository provides
  the `High` security commitments level as defined here, with a link to this
  section.
