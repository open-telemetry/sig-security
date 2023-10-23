# Recommendations

This document lists recommendations from the Security SIG for
the consideration of OpenTelemetry SIGs.

## CodeQL Scanning

The organization uses [CodeQL](https://codeql.github.com/) for semantic analysis
of the code in various repositories. The recommendation is to run CodeQL on every
pull request and on every commit to the main branch.

Issue: ([#15](https://github.com/open-telemetry/sig-security/issues/15))

## Binding to Network Interfaces
Always bind to localhost rather than to 0.0.0.0 or any interface, unless there is a specific need to do otherwise. Binding to localhost reduces the attack surface of your application by making it only accessible to devices on the same machine.
Binding to 0.0.0.0 or "all" interfaces can make your application respond on all current and future network interfaces.

**Rationale:**
* OTel is a powerful tool that can be used to collect and analyze data from a variety of sources. This data can be sensitive, so it is important to protect it from unauthorized access.
* Binding to localhost will prevent OTel from being exposed to attackers who are scanning the public internet for vulnerable systems.
* Binding to localhost will also make it more difficult for attackers to exploit vulnerabilities in OTel.

Issue: ([#19](https://github.com/open-telemetry/sig-security/issues/19#issue-1926445623))
