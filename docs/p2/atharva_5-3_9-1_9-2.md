## 5.3 Consistency cross-check

| Check | Result (pass, or what failed) | Fixed in |
| :--- | :--- | :--- |
| **K1** Every item in an actor column (4.2) is an attribute in the domain model (5.1) | Pass | N/A |
| **K2** Every object on a sequence diagram is a domain class or a declared interaction object | Pass | N/A |
| **K3** Every message on a sequence diagram corresponds to exactly one scenario-table row | Pass | N/A |
| **K4** Every non-trivial step in 5.2 (a) has at least one scenario-table row | Pass | N/A |
| **K5** Every analyzed use case traces to at least one functional requirement | Pass | N/A |
| **K6** The last messages of each diagram make the use case postcondition true | Fail (the postcondition for UC-01 says the student sees the filtered list, but figure 5.2.1 displays the last message 4b, which says that the website “adds the next 20 matching events”) | Fixed in 4.2, changed the wording of the postcondition to match the 5.2.1 diagram |


## 9.1 Extended traceability matrix 

| Requirement | Use case | Analysis classes | Component(s) | QAS / ADR | Evidence | 
| :--- | :--- | :--- | :--- | :--- | :--- | 
| **FR-01** | UC-01 | Event, SourceListing | C2, C3 | ADR-01, ADR-03 | S-01 | 
| **FR-02** | UC-01 | Event, Tag | C3 | ADR-01, ADR-03 | None yet (website development in progress) | 
| **FR-03** | UC-03 | Event, SourceListing, SourceSite | C1, C2 | ADR-02, ADR-03 | None yet (website development in progress) | 
| **FR-04** | UC-06 | SourceSite | C3 | ADR-03 | None yet (website development in progress) | 
| **FR-05** | UC-01, UC-05 | Event, SourceListing, SourceSite | C1, C2, C3 | ADR-02, ADR-03 | None yet (website development in progress) | 
| **FR-06** | UC-04 | Event | C3, C4 | ADR-01, ADR-03 | None yet (website development in progress) |
| **FR-07** | UC-01, UC-02, UC-03 | Event, Organizer, Tag, SourceListing | C3 | ADR-01, ADR-03 | None yet (website development in progress) | 
| **FR-08** | UC-05 | Event, Organizer | C3 | ADR-01, ADR-03 | None yet (website development in progress) | 
| **FR-09** | UC-02, UC-03 | Event, SourceListing | C3 | ADR-01, ADR-03 | None yet (website development in progress) | 
| **FR-10** | UC-02 | SharedLink, Event | C3 | ADR-01, ADR-03 | None yet (website development in progress) | 
| **FR-11** | UC-01 | Event | C2, C3 | ADR-01, ADR-03 | None yet (website development in progress) | 
| **FR-12** | UC-02, UC-03 | Event, SourceSite, SourceListing | C3 | ADR-01, ADR-03 | None yet (website development in progress) | 
| **QR-01** | UC-01 | Event | C3 | QAS-01, ADR-01, ADR-03 | None yet (website development in progress) | 
| **QR-02** | UC-01 | Event, Tag | C3 | QAS-01, ADR-01, ADR-03 | None yet (website development in progress) | 
| **QR-03** | UC-01, UC-02 | Event, SourceSite | C1 | ADR-02 | None yet (website development in progress) | 
| **QR-04** | UC-01, UC-02, UC-03 | Event, SourceListing | C1, C2 | ADR-02 | None yet (website development in progress) | 
| **QR-05** | UC-03 | Event | C3 | ADR-01 | None yet (website development in progress) | 
| **QR-06** | UC-01 | Event, SourceSite, SourceListing | C2 | ADR-02, ADR-03 | None yet (website development in progress) | 
| **CON-01** | | | C3 | ADR-01 | None yet (website development in progress) | 
| **CON-02** | UC-01, UC-03 | SourceSite, SourceListing | C1 | ADR-02 | None yet (website development in progress) | 
| **CON-03** | UC-01 | SourceSite | C1 | ADR-02 | None yet (website development in progress) | 
| **CON-04** | | | C1, C2, C3, C4 | ADR-03 | None yet (website development in progress) |


## 9.2 Gap analysis 
| Gap | Items | What you did about it |
| :--- | :--- | :--- | 
| Requirements with no component | N/A (All requirements have at least 1 component) | |
| Components with no requirement, QAS or ADR | N/A (All components have a requirement, QAS, or ADR) | |
| Use cases not analyzed (and why that is acceptable) | N/A (Each UC corresponds to at least 1 requirement) | |
