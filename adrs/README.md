# Architecture Decision Records (ADRs)

[Architecture Decision Records][adrs] (ADRs) are a way to document the
decisions made within the Security SIG.

The purpose of documenting these decisions isn't to add complexity, or require
some gate, or architecture review board. It's simply to provide a written
record with context on the decisions made. As humans, we forget, so having a
written record can simply help us to remember.

## Getting Started

To make a new ADR, you can use the `adr-new` make target. This will create a
new ADR with the branch name and the date.

```bash
make adr-new
```

From there you can edit your template in the [./adrs/](./adrs/) directory.

[adrs]: https://github.com/joelparkerhenderson/architecture-decision-record
