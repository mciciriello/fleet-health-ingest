# Status

Living session handoff. Update this file at the end of every working session. Keep it as project notes, not a diary. No personal details.

## Last session

**2026-09-22.** Named the estate (wired / navi / Layer). Public brief, glossary, session skill (Linux-first teaching), operator tour, scratchpad first picture. Stay on the local lab. AWS waits.

## Done

- FastAPI ingest: `POST /ingest`, `GET /latest`, `GET /health`
- MariaDB schema `wired.health_events` plus Grafana dashboard **Layer** (Latest table only)
- Docker Compose lab (project `wired`: ingest + MariaDB + Grafana)
- Pytest in CI; image build and push to GHCR on `main`
- Dual-audience README, [GLOSSARY.md](GLOSSARY.md), [NAMING.md](NAMING.md), git-tracked Cursor handoff
- Operator tour: [docs/layer-tour.html](docs/layer-tour.html)
- Scratchpad: [scratchpad/wired-first-picture.md](scratchpad/wired-first-picture.md)

## Next

Local first. Do not start AWS until Layer is a panel you would leave open.

1. Bring wired up (`docker compose up` in the LXC). POST. See a row in Layer.
2. Sender under systemd (Python). Then navi-01 .. navi-03 posting every few minutes.
3. Grow Layer (glance counts, sick row first) toward the tour.
4. Later: AWS account hygiene, then Terraform. Same wired, rented.

## Blockers

None. Local Compose needs Docker Engine **inside the LXC lab**, not on the workstation host.

## Out of scope

Kubernetes, a second cloud, vendor monitoring protocols, installing lab tools on the host.
