# Security Response Committee (SRC)

The SRC is responsible for organizing the entire response including internal
communication and external disclosure but will need help from relevant
developers and release managers to successfully run this process.

## Security Response Committee Membership

New SRC members are nominated by current SRC members, and selected by [TBD]

The SRC is capped at 10 members.

### Nomination

New members are nominated to the SRC by current SRC members. If you are
interested in joining the SRC, the best way to secure a nomination is through
sustained participation and contributions in the OpenTelemetry community.

To encourage diversity members will also abide by a 1/2 maximal representation
from any one company at any time. If representation changes due to job shifts or
mergers, then members are encouraged to grow the team or replace themselves
through mentoring new members. Being overlimit should not continue for longer
than 12 months to give time to identify and mentor new members.

A nomination should include:

1. Relevant credentials, including OpenTelemetry and security experience.
2. Statement of support from the nominating SRC member(s): ~1-3 sentences of why
   this person is a good candidate.
3. Statement of intent from the nominee: ~1-3 sentences of why they want to join
   the committee and are a good fit.

In the event that an SRC member has concerns with a nomination, they should
privately reach out to [TBD].

Nominations will be collected into a private Google doc shared between the SRC
and Steering.

Nominations may be reused for new openings, but in that case both the SRC member
and nominee should reconfirm (or update) their statements.

### Member selection

After the nomination deadline is passed, nominations will be shared with the
Steering Committee. Steering is encouraged to discuss the nominations in the
next private monthly meeting, and reach out to the SRC with any questions.

The final selection is made by discussion & lazy consensus, with a fallback to a
vote.

In the event that an individual is on both the SRC and Steering Committee, they
will be expected to excuse themselves from the steering discussion & selection
process (but may submit SRC nominations).

### Stepping Down

Members may step down at anytime, and may nominate a replacement when they do.

### Responsibilities

- Members should remain active and responsive, and participate in the [oncall
  rotation](./src-oncall.md).
- Members going on extended leave for up to 3 months (1-2 rotations) may pause
  their oncall duties, but should coordinate with other members to ensure the
  role is adequately staffed during the leave.
- Longer leaves of absense should be discussed on a case-by-case basis.
- Members of a role should remove any other members that have not communicated a
  leave of absence and either cannot be reached for more than 2 months or are
  not fulfilling their documented responsibilities for more than 2 months. This
  may be done through a super-majority vote of members.

New members are *not* expected to join the oncall rotation immediately, but are
expected to start learning the processes and ramping up. During that time, they
are expected to complete a shadow and reverse shadow rotation. The ramp-up time
does not need to be formalized, but 2-3 months should be a reasonable
expectation.

#### Incident Commander

One of the primary responsibilities of the SRC is to coordinate incident
response when a vulnerability is discovered. The incident commander is
responsible for coordinating all the different parts of the security release
process (but not handling all those responsibilities themselves), and seeing the
incident through to the end (or handing off).

The incident commander defaults to the current oncall, but may be handed off to
other SRC or OpenTelemetry maintainers.

#### Triage

The current oncall is responsible for triaging incoming vulnerability reports
(both through the bug bounty and email). For more details on the triage process,
see [oncall workflow](./src-oncall.md).
