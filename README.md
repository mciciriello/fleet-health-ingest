# fleet-health-ingest

A small observability ingest lab: hosts POST generic health samples, MariaDB stores them, Grafana charts them. The same app then gets a cloud delivery layer (containers, CI, Terraform on AWS).

This is a working pipeline you can run, not a tutorial dump and not a clone of any vendor monitoring product. Generic JSON only. No customer data.

![ci](https://github.com/mciciriello/fleet-health-ingest/actions/workflows/ci.yml/badge.svg)

Session handoff: [STATUS.md](STATUS.md). Agent notes: [AGENTS.md](AGENTS.md). Lexicon: [GLOSSARY.md](GLOSSARY.md). Lab names: [NAMING.md](NAMING.md). Operator tour (wireframe): [docs/layer-tour.html](docs/layer-tour.html).

## Why this exists

Monitoring estates share one shape: something reports in, something stores it, something you can look at. This repo is that shape in the open, with the platform work around it made visible.

- **The app:** HTTP ingest, MariaDB, Grafana.
- **The delivery layer:** Docker Compose locally, GitHub Actions for test and image publish, Terraform on AWS next (VPC, IAM, S3, ECS or one EC2, ALB, CloudWatch, deploy via OIDC).

If you are hiring: you can clone it, run it, and see how far the cloud path has got. If you are picking this up again: start at [STATUS.md](STATUS.md).

## Pipeline

```
host or curl  --POST JSON-->  FastAPI ingest  -->  MariaDB
                                                    ^
Grafana dashboard  ---------------------------------+
```

Payload:

```json
{"host":"navi-01","cpu_pct":12.4,"mem_pct":41.0,"ok":true}
```

## Stack

| Piece | Role |
|---|---|
| FastAPI (`ingest`) | Accepts and validates health POSTs; `GET /latest` for a quick read |
| MariaDB | Stores rows in `wired.health_events` |
| Grafana | Dashboard **Layer** (anonymous viewer in the lab) |
| Docker Compose | Local lab: ingest + store + dashboard in one command |
| GitHub Actions | Pytest, build, push `ghcr.io/mciciriello/fleet-health-ingest` |
| Terraform on AWS | Next: VPC, IAM, S3, ECS (or EC2), ALB, CloudWatch, Actions OIDC |

**Not in this lab:** Kubernetes, a second cloud, vendor agent protocols.

## Where it runs

Local work runs **inside a Linux container (LXC)** so the workstation host stays clean. Docker Engine must be available **in that container**, then Compose as below. Do not install Docker, Terraform, or AWS CLIs on the host.

Compose passwords (`ingest` / `grafana` / `admin`) are lab defaults. Do not reuse them on AWS.

## Status

| Layer | State |
|---|---|
| App + Compose + Grafana | In repo. `docker compose up` is the local proof |
| Pytest + GHCR image | CI on `main` |
| AWS + Terraform + OIDC | Next. See [STATUS.md](STATUS.md) |

## What is in the box

| Piece | Port | What it does |
|---|---|---|
| `ingest` | 8080 | FastAPI. `POST /ingest`, `GET /latest`, `GET /health` |
| `mariadb` | 3306 | Stores rows in `wired.health_events` |
| `grafana` | 3000 | Dashboard **Layer** (anonymous viewer) |

## Run locally

From the LXC lab, Docker Compose or Podman with the compose plugin.

```bash
docker compose up --build
```

In another terminal:

```bash
curl -sS http://127.0.0.1:8080/health
./scripts/post-sample.sh
```

Open [http://127.0.0.1:3000/d/layer/layer](http://127.0.0.1:3000/d/layer/layer). You should see `navi-01`. Grafana login is `admin` / `admin` if anonymous view is not enough.

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

Terraform on AWS: VPC, IAM, S3, ECS (or EC2), Actions deploy via OIDC. Concrete next step lives in [STATUS.md](STATUS.md).

## API

| Method | Path | Notes |
|---|---|---|
| GET | `/health` | Process up. Does not need the database |
| POST | `/ingest` | Body: `host`, `cpu_pct` 0-100, `mem_pct` 0-100, `ok` |
| GET | `/latest?limit=20` | Newest rows first |
