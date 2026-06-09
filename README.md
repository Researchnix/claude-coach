# claude-coach

A collection of Claude commands and python scripts to automate a Claude running and cycling coach with data collected on a Garmin device.

## Architecture

```mermaid
flowchart TD
    G[garmin.py] --> S[sync.py]
    I[intervals.py] --> S
    P[parser.py] --> S
    S --> DB[(db.py\nSQLite)]
    DB --> PR[processor.py]
    PR --> C[Claude skill]
```

### Modules

| module | responsibility |
|---|---|
| `garmin.py` | fetch activities and FIT files from Garmin Connect |
| `intervals.py` | fetch activities and push planned workouts to Intervals.icu |
| `parser.py` | parse FIT files into metrics dicts |
| `sync.py` | pull from both sources, match activities, fill gaps, write to db |
| `db.py` | SQLite schema, upsert and query functions |
| `processor.py` | query db, format data as markdown tables for Claude |
