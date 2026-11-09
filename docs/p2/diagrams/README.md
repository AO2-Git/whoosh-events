# P2 diagram sources

All diagrams below are drawn from one script, so they can be regenerated after any change:

```bash
python3 draw_diagrams.py   # needs matplotlib
```

| File | Figure in the P2 document | Drawn from |
|---|---|---|
| `context_diagram.png` | 2.1 Context diagram | boundary paragraph in 2.1 |
| `use_case_diagram.png` | 3.4 Use case diagram | actor-goal list in 3.4 |
| `domain_model.png` | 5.1 Domain model | class table in 5.1 |
| `sd_uc01.png` | 5.2.1 Analysis sequence diagram, UC-01 Find Events by Tag | scenario table in 5.2.1 (b) |
| `sd_uc02.png` | 5.2.2 Analysis sequence diagram, UC-02 Share an Event with a Friend | scenario table in 5.2.2 (b) |

The sequence diagrams are generated row by row from the `UC01` and `UC02` lists in the script, so every
message number matches a scenario-table step number (check K3 in 5.3).
