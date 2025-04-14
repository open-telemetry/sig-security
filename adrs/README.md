# Architecture Decision Records (ADRs)

[Architecture Decision Records][adrs] (ADRs) are a way to document the
decisions made within the Security SIG.

The purpose of documenting these decisions isn't to add complexity, or require
some gate, or architecture review board. It's simply to provide a written
record with context on the decisions made. As humans, we forget, so having a
written record can simply help us to remember.

## Getting Started

1. Review the [CONTRIBUTING.md][ctrb] document for general contributing
   guidelines.
2. In your fork, create a new branch for your ADR.
3. Use the `adr-new` make target. This will create a new ADR with the branch
   name and the date.

```bash
make adr-new
```

4. Edit your template in the [./adrs/](./adrs/) directory.
5. Open a pull request against the `main` branch from your fork.

[ctrb]: ../CONTRIBUTING.md
[adrs]: https://github.com/joelparkerhenderson/architecture-decision-record
