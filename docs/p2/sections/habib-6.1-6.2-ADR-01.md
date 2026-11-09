# P2 sections by Habib Mashhood: 6.1, 6.2 and ADR-01

## 6.1 Architectural drivers: quality-attribute scenarios

| QAS | Quality attribute | Stimulus | Artifact | Response | Response measure | From |
|---|---|---|---|---|---|---|
| QAS-01 | Performance | A student opens the event list, or applies a tag filter, on a 10 Mbps connection with 50 ms latency | C3 Website on Vercel | Shows the first 20 event cards, or the filtered list | Page finishes loading within 3 s on at least 19 of 20 loads | QR-01, QR-02 |
| QAS-02 | Timeliness | An organizer posts a new event on the UTD Calendar or Nebula site | C1 Event Collector and the stored events.json | The event is collected, saved and shown on the site | Within 2 hours for at least 9 of 10 new events | QR-03 |
| QAS-03 | Availability | One source site cannot be reached during a scheduled refresh | C1 Event Collector and C2 Event Storage | Events from that site's last good refresh stay in events.json and stay on the site | 100% of that site's previously listed events still shown after the failed refresh | QR-06 |

Constraints shaping the architecture: CON-01 (users cannot create events, so the site is read-only), CON-02 (only the two source sites), CON-03 (robots.txt rules), CON-04 (free hosting only).

## 6.2 Architectural style and alternatives

| Style considered | Drivers it serves | What it costs | Verdict |
|---|---|---|---|
| Repository (shared data file) with a scheduled batch collector; browsers talk to a static site (client-server) | QAS-01, QAS-02, QAS-03, CON-04 | Events can be up to one refresh old. The site redeploys on each refresh. The collector must remove duplicates (FR-03). | Chosen |
| Client-server with live fetch: the site calls both source sites on every page view | QAS-02 (always current) | Page speed depends on two outside sites (breaks QAS-01). No stored copy, so a source outage gives an empty list (breaks QAS-03). Needs an always-on server (CON-04). | Rejected |
| Event-driven / microservices: separate services connected by a message queue | Scaling and easy change | The source sites send no push events, so there is nothing to react to. Several hosted services will not fit a free plan (CON-04). Too much for a 6-person team to build by December. | Rejected |

We chose the repository style because the three scenarios all depend on keeping a saved copy of the events. The collector (C1) writes events.json on a schedule and the website (C3) only reads it, so the page speed in QAS-01 does not depend on the source sites. A refresh within an hour or two meets QAS-02. A failed refresh leaves the saved file unchanged, which meets QAS-03. Live fetching has no saved copy and cannot meet QAS-01 or QAS-03. Event-driven or microservice designs add parts and cost that CON-04 and our team size do not allow.

## ADR-01 Architectural style

| Row | Text |
|---|---|
| Status | Accepted |
| Date and owner | 11/4/2026 \| Habib Mashhood |
| Context (drivers) | QAS-01, QAS-02 and QAS-03 all need a saved copy of the events. CON-02 and CON-03 limit how we may read the sources. CON-04 requires free hosting. CON-01 makes the site read-only. |
| Options considered | 1. Repository style: a scheduled collector writes events.json and the website reads it. 2. Client-server with live fetch from the source sites on every page view. 3. Event-driven or microservices with a message queue. |
| Decision | Use the repository style. C1 runs on a schedule and writes events.json. C3 reads only that file. C1 and C3 never call each other. |
| Consequences | Favors QAS-01 (the page reads our own file) and QAS-03 (a failed run leaves the file unchanged). Move: collecting and showing are separate, joined only by events.json. Cost: events can be up to one refresh interval old, and every refresh redeploys the site. |
| Evidence | Spike S-01 (section 8) measures a real scrape of both sources. Open question: does a scheduled run finish within the 2-hour limit in QAS-02? |
| Related | ADR-02, ADR-03, QAS-01, QAS-02, QAS-03, R1 |
