# SIG Security Charter

## Scope

SIG Security covers horizontal security initiatives for the OpenTelemetry (OTel)
project and is focused on improving the security of the project across all
components.

This includes preparing the project for regular security audits, improving the
vulnerability management process, producing cross-cutting security
documentation, serving as a security community touch point, managing the
non-emnargoed (public) vulnerability process, default repo configurations, and
defining the bug bounty.

As a process-oriented SIG, SIG Security does not directly own OpenTelemetry component
code.

### In scope

#### Vulnerability Management Process

Work with the OpenTelemetry Technical Committee (TC) to define the processes for fixing and disclosing vulnerabilities. For example:

- The default level for OTel repo Github security configuration and tooling
- When the private fix & release process is invoked
- How vulnerabilities are rated
- The scope of the bug bounty
- Post-announcement follow-ups, such as additional fixes, mitigations, preventions or documentation after a vulnerability is made public
- Distributor announcement policies, such as timelines, criteria for joining the list, etc.
- How, when and where vulnerabilities are announced

#### Security Community Management and Outreach

Provide an entry point to the OTel community for new security-minded contributors, as well as a meeting point to discuss security themes and issues within OTel, including:

- Answer security questions from inexperienced users (that don't know what SIG to go to), and identify common questions or issues as areas for improvement.
- Provide an "entry point" for new contributors interested in security. Route these new contributors to other SIGs when they have more specific goals (e.g. SIG Node for container isolation).

#### Horizontal Security Documentation

Author and maintain cross-cutting security documentation. Seek out and coordinate with experts in other SIGs for input on the documentation (i.e. we go to them, they don't need to come to us). In-scope documentation includes:

- TBD

#### Security Audit

Manage recurring CNCF security audits and follow up on issues. Coordinate vendors to perform the audit and publish the findings. Follow up on issues with the affected SIG and help coordinate resolution, which can include:

- Helping to prioritize the fixes, possibly by recruiting from SIG Security (while acknowledging that the ultimate authority in deciding whether and how to fix an issue lies with the responsible SIG).
- Documenting mitigations, workarounds, or caveats, especially when the responsible SIG decides not to fix a reported issue.

### Out of scope

SIG Security’s scope does not include:

- Developing any new telemetry signals, SDKs, APIs etc.
- Security audit for other CNCF projects (e.g., etcd, CoreDNS, CRI-O, containerd) (Belongs to the CNCF’s SIG Security.)
- Any projects outside of the OpenTelemetry project and community repos
- Vendor or distribution specific guidelines and vulnerability coverage
- Recommendations or endorsements of specific commercial product vendors or cloud providers
- Private vulnerability response (belongs to the PSC), including:
  - Embargoed vulnerability management
  - Bug bounty submission triage and management
  - Non-public vulnerability collection, triage, and disclosure
