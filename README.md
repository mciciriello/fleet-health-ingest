# fleet-health-ingest

Small observability ingest lab. HTTP POST of generic host health, MariaDB store, Grafana read.

This is personal skill-up for the US keyword screen: **Docker, GitHub Actions, then AWS**. It is not a work platform and it does not speak any vendor monitoring protocol.

![ci](https://github.com/mciciriello/fleet-health-ingest/actions/workflows/ci.yml/badge.svg)

## What is in the box

| Piece | Port | What it does |
|---|---|---|
| `ingest` | 8080 | FastAPI. `POST /ingest`, `GET /latest`, `GET /health` |
| `mariadb` | 3306 | Stores rows in `fleet.health_events` |
| `grafana` | 3000 | Dashboard **Fleet health** (anonymous viewer) |

Payload shape:

```json
{"host":"lab-01","cpu_pct":12.4,"mem_pct":41.0,"ok":true}
```

Local compose passwords (`ingest` / `grafana` / `admin`) are lab defaults. Do not reuse them on AWS.

## Week 1: run it on this machine

You need Docker Compose **or** Podman with the compose plugin. This repo's author machine had Podman 4.9 and no Docker yet. Either is fine. The file is still `docker-compose.yml` because that is the name recruiters look for.

```bash
cd ~/CODE/fleet-health-ingest
docker compose up --build
# or: podman-compose up --build
```

Wait until ingest is listening. Then in another terminal:

```bash
curl -sS http://127.0.0.1:8080/health
./scripts/post-sample.sh
```

Open [http://127.0.0.1:3000/d/fleet-health/fleet-health](http://127.0.0.1:3000/d/fleet-health/fleet-health). You should see `lab-01`. Grafana login is `admin` / `admin` if anonymous view is not enough.

**Done when:** a row you posted shows in Grafana.

## Tests without Compose

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r ingest/requirements.txt -r ingest/requirements-dev.txt
cd ingest && pytest
```

## Week 2: CI

Every push to `main` runs pytest and builds the ingest image. On `main` it also pushes `ghcr.io/mciciriello/fleet-health-ingest`.

## Later (not this commit)

Terraform, AWS VPC/IAM/S3/ECS, Actions deploy via OIDC. See the desk page `roles/it-tools-and-automation/cloud-spec.md` in `it-tanda-consultant`.

## API

| Method | Path | Notes |
|---|---|---|
| GET | `/health` | Process up. Does not need the database |
| POST | `/ingest` | Body: `host`, `cpu_pct` 0-100, `mem_pct` 0-100, `ok` |
| GET | `/latest?limit=20` | Newest rows first |
