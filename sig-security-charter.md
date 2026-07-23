# SIG Security Charter

## Scope

SIG Security covers horizontal security initiatives for the OpenTelemetry (OTel)
project and is focused on improving the security of the project across all
components.

This includes:

* preparing the project for regular security audits
* improving the vulnerability management process
* producing cross-cutting security documentation
* serving as a security community touch point
* default repo configurations related to security

As a process-oriented SIG, SIG Security does not directly own OpenTelemetry
component code.

### In scope

#### Vulnerability Management Process

Work with the OpenTelemetry Technical Committee (TC) to define the processes for
fixing and disclosing vulnerabilities. For example:

* The default OTel repo GitHub security configuration and tooling
* When the private fix & release process is invoked
* How vulnerabilities are rated
* Post-announcement follow-ups, such as additional fixes, mitigations,
  preventions or documentation after a vulnerability is made public
* Distributor announcement policies, such as timelines, criteria for joining the
  list, etc.
* How, when and where vulnerabilities are announced

#### Security Community Management and Outreach

Provide an entry point to the OTel community for new security-minded
contributors, as well as a meeting point to discuss security themes and issues
within OTel, including:

* Answer security questions from inexperienced users (that don't know what SIG
  to go to), and identify common questions or issues as areas for improvement.
* Provide an "entry point" for new contributors interested in security. Route
  these new contributors to other SIGs when they have more specific goals (e.g.
  SIG Node for container isolation).

#### Horizontal Security Documentation

Author and maintain cross-cutting security documentation. Seek out and
coordinate with experts in other SIGs for input on the documentation (i.e. we go
to them, they don't need to come to us). In-scope documentation includes:

* Best practices for secure development lifecycle
* Authentication and authorization
* Secret management
* Storage security
* Supply chain security
* Transport security

#### Security Audit

Manage recurring CNCF security audits and follow up on issues. Coordinate
vendors to perform the audit and publish the findings. Follow up on issues with
the affected SIG and help coordinate resolution, which can include:

* Helping to prioritize the fixes, possibly by recruiting from SIG Security
  (while acknowledging that the ultimate authority in deciding whether and how
  to fix an issue lies with the responsible SIG).
* Documenting mitigations, workarounds, or caveats, especially when the
  responsible SIG decides not to fix a reported issue.

### Out of scope

SIG Security's scope does not include:

* Developing any new telemetry signals, SDKs, APIs etc.
* Defining security semantic conventions
* Security audit for other CNCF projects (e.g., etcd, CoreDNS, CRI-O,
  containerd). These belong to the [CNCF's SIG
  Security](https://github.com/cncf/tag-security).
* Any projects outside of the OpenTelemetry project and community repos
* Vendor or distribution specific guidelines and vulnerability coverage
* Recommendations or endorsements of specific commercial product vendors or
  cloud providers
* Direct vulnerability response, this belongs to the relevant repo owners.

## Membership, Roles, and Responsibilities

SIG Security is open to all OpenTelemetry contributors and community members
interested in security. We welcome all levels of experience, from those who are
new to security to those who are seasoned experts. We encourage participation
from a diverse range of backgrounds and perspectives, as security is a
multifaceted field that benefits from a variety of viewpoints.

Currently, we have the
[sig-security-maintainers](https://github.com/orgs/open-telemetry/teams/sig-security-maintainers)
and
[sig-security-approvers](https://github.com/orgs/open-telemetry/teams/sig-security-approvers)
groups following the [OpenTelemetry community
guides](https://github.com/open-telemetry/community/blob/main/guides/contributor/membership.md).

Due to the nature of the work, we hold a higher bar for maintainers because they
have access to very sensitive information. In addition to the requirements
described in the [general
guides](https://github.com/open-telemetry/community/blob/main/guides/contributor/membership.md#becoming-a-maintainer),
we require explicit discussion and agreement from the [Governance
Committee](https://github.com/open-telemetry/community/blob/main/community-members.md#governance-committee)
and the [Technical
Committee](https://github.com/open-telemetry/community/blob/main/community-members.md#technical-committee).
