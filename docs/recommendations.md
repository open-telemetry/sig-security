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

Issue: ([#19](https://github.com/open-telemetry/sig-security/issues/19#issue-1926445623))
