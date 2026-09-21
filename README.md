# fleet-health-ingest

Observability ingest lab: HTTP POST of generic host health, MariaDB store, Grafana read.

Docker Compose locally. GitHub Actions builds the image. AWS deploy comes next.

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

Compose passwords (`ingest` / `grafana` / `admin`) are lab defaults. Do not reuse them on AWS.

## Run locally

Docker Compose or Podman with the compose plugin.

```bash
docker compose up --build
```

In another terminal:

```bash
curl -sS http://127.0.0.1:8080/health
./scripts/post-sample.sh
```

Open [http://127.0.0.1:3000/d/fleet-health/fleet-health](http://127.0.0.1:3000/d/fleet-health/fleet-health). You should see `lab-01`. Grafana login is `admin` / `admin` if anonymous view is not enough.

## Tests without Compose

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r ingest/requirements.txt -r ingest/requirements-dev.txt
cd ingest && pytest
```

## CI

Every push to `main` runs pytest and builds the ingest image. On `main` it also pushes `ghcr.io/mciciriello/fleet-health-ingest`.

## Next

Terraform on AWS: VPC, IAM, S3, ECS (or EC2), Actions deploy via OIDC.

## API

| Method | Path | Notes |
|---|---|---|
| GET | `/health` | Process up. Does not need the database |
| POST | `/ingest` | Body: `host`, `cpu_pct` 0-100, `mem_pct` 0-100, `ok` |
| GET | `/latest?limit=20` | Newest rows first |
