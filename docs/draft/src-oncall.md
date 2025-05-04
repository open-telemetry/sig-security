# Security Response Committee Oncall

Security Response Committee (SRC) Oncall is a business-hours only oncall. That
means you are not expected to respond to issues outside of your normal daily
working hours or on weekends or holidays. If you are taking vacation or will be
unable to perform your oncall duties, please swap oncalls or find coverage for
that week. See [managing oncall rotation](#appendix-managing-oncall-rotation).

<!-- toc -->
- [Responsibilities](#responsibilities)
- [Triage Workflow](#triage-workflow)
- [Incident Response Workflow](#incident-response-workflow)
- [Handoff](#handoff)
- [Appendix: Managing Oncall Rotation](#appendix-managing-oncall-rotation)
  - [Adding the rotation to your
    calendar](#adding-the-rotation-to-your-calendar)
  - [Swapping shifts or adding coverage](#swapping-shifts-or-adding-coverage)
<!-- /toc -->

## Responsibilities

Daily:

- Triage vulnerability reports. We target 1 business day for initial response.
  - [TBD]

- Handle incident response for ongoing issues
  - Drive progress on assigned issues. Query: [TBD]
    - See [incident response](#incident-response-workflow) for details
  - Ping incident commander of critical issues, if last update > 2 days ago.
    Query: [TBD]

Weekly (ideally at the beginning of your shift):

- Ping incident commander of high severity issues, if last update was > 7 days
  ago.  Query: [TBD]

- Ping incident commander of medium severity issues, if last update was > 1
  month ago.  Query: [TBD]

- Check for new issues in this repository, especially distributor list join
  requests. Triage, assign or handle new issues, as appropriate.  Query: [TBD]

- Check for new PRs in this repository and address open PRs where possible.
  Query: [TBD]

## Triage Workflow

[TBD] Update Chart... ![Triage workflow
flowchart](images/src-oncall-triage-flow.png)

## Incident Response Workflow

[TBD] Update Chart... ![Incident response
flowchart](images/src-oncall-incident-flow.png)

## Handoff

When your shift ends, you may be the incident commander on one or more ongoing
incidents. If you are already invested in the incident and have the bandwidth
for it, you can continue managing the incident (thanks!), but _you are not
obligated to continue managing the incident!_

If you would like to handoff incident command:

1. Start by **ensuring the tracking issue is up to date** - review the
   information in the issue description, and fill in or correct any missing
   details.
2. **Leave a comment** to dump any additional context and state you have on the
   issue. Make sure to list any open questions or decisions and any pending
   action items.
3. Reassign the issue to the next oncall.

Finally, reach out to the next oncall (email, slack, VC, your choice) to make
sure they're aware of the handoff and to answer any questions. _Until they've
explicitly acknowledged the handoff you are still the incident commander!_

## Appendix: Managing Oncall Rotation

### Adding the rotation to your calendar

[TBD]

### Swapping shifts or adding coverage

[TBD]
