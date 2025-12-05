
## Quick dev run (after these new files)

# 1) initialize DB
python3 backend/migrations/init_db.py

# 2) start backend (from repo root)
python3 -m backend.main

# 3) test ingest
curl -X POST "http://0.0.0.0:8000/ingest" -H "Content-Type: application/json" -d '{"source":"test","type":"note","timestamp":1730000000,"content":"test event from CLI","metadata":{"tag":"dev"}}'

# 4) test long-term memory
curl -X POST "http://0.0.0.0:8000/moats/long_term_memory/run" -H "Content-Type: application/json" -d '{"top_k":200,"granular":true}'

# 5) test graph
curl -X POST "http://0.0.0.0:8000/moats/behavior_graph/run" -H "Content-Type: application/json" -d '{"top_k":200}'

