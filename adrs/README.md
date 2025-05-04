# Architecture Decision Records (ADRs)

[Architecture Decision Records][adrs] (ADRs) are a way to document the
decisions made within the Security SIG. These decisions ARE NOT intended to be
mandates across the OpenTelemetry project, nor are they hard requirements. The
focus is mainly to provide context around various decisions made within the SIG
so that others can easily access that context as a written record.

ADRs SHOULD:

* Document something of importance and the surrounding context.
* Be updated and reviewed at an interval.
* Be light-weight, easy to write, and clear.

## Getting Started

1. Review the [CONTRIBUTING.md][ctrb] document for general contributing
   guidelines.
2. In your fork, create a new branch for your ADR, with a meaningful branch
   name that correctly reflects the subject of your ADR.
3. Run `make adr-new` to create a new ADR with a file name of `<date>-<branch>.md`.
4. Edit your template in the [./adrs/](./adrs/) directory.
5. Open a pull request against the `main` branch from your fork.

[ctrb]: ../CONTRIBUTING.md
[adrs]: https://github.com/joelparkerhenderson/architecture-decision-record
