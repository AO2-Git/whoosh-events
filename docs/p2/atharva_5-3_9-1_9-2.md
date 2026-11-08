## 5.3 Consistency cross-check

| Check | Result (pass, or what failed) | Fixed in |
| :--- | :--- | :--- |
| **K1** Every item in an actor column (4.2) is an attribute in the domain model (5.1) | Pass | N/A |
| **K2** Every object on a sequence diagram is a domain class or a declared interaction object | Pass | N/A |
| **K3** Every message on a sequence diagram corresponds to exactly one scenario-table row | Pass | N/A |
| **K4** Every non-trivial step in 5.2 (a) has at least one scenario-table row | Pass | N/A |
| **K5** Every analyzed use case traces to at least one functional requirement | Pass | N/A |
| **K6** The last messages of each diagram make the use case postcondition true | Fail (the postcondition for UC-01 says the student sees the filtered list, but figure 5.2.1 displays the last message 4b, which says that the website “adds the next 20 matching events”) | Fixed in 4.2, changed the wording of the postcondition to match the 5.2.1 diagram |
