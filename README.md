# Personal ISP Monitor — Project A

A **local, single-machine TCP-connect monitor** with SQLite storage, FastAPI REST endpoints and a zero-build browser dashboard. Intended as a reproducible learning project, not an independently verified ISP report.

## Requirements
Python 3.10+ (3.12 recommended), internet connection for real probe targets.

## Install (PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
On Linux/macOS: `python3 -m venv .venv && source .venv/bin/activate`.

## Run (two terminal windows in the project folder)
```powershell
python -m monitor.agent --count 10
```
```powershell
uvicorn monitor.api:app --reload
```
Open http://127.0.0.1:8000 and http://127.0.0.1:8000/docs. To monitor continually, omit `--count 10`.

## Configuration
Copy `.env.example` for reference. This starter reads real environment variables, **not** `.env` automatically. In PowerShell set, for example, `$env:PROBE_HOST='1.1.1.1'`; `$env:PROBE_INTERVAL_SECONDS='60'`. Default TCP target is `1.1.1.1:443`. Probe a host/service you are authorized to test. `DATABASE_PATH` changes DB location.

## Test
`python -m pytest -q`

## Scope and limitations
- `connect_ms` is **TCP connection-establishment time**, not ICMP ping, end-to-end application latency, jitter, packet loss or bandwidth.
- `observed_success_pct` is a proportion of successful samples, **not a certified uptime SLA**. Intervals between probes may contain downtime.
- DNS resolution, Wi-Fi problems, endpoint outages, rate limiting and network routing can skew conclusions. ISP attribution requires evidence beyond one endpoint.
- No active large-data download/upload speed testing is included; avoid accidental mobile-data consumption.
- DB stores test targets/errors and timestamps, not personal browsing history.
- This is intentionally lightweight with one API process and one agent process. Do not expose this starter API directly to the public internet.

## API
`GET /api/health`, `GET /api/measurements?limit=100`, `GET /api/summary?limit=100`.

## Learning path
Read `docs/REBUILD_STEP_BY_STEP.md` and accompanying Network Learning Handbook. The build guide specifies exactly which files to create in what order.
