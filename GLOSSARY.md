# Glossary

Lexicon for this lab. Meaning, then how it shows up here. Not a tutorial.

Lab identifiers (`wired`, `navi-01`, dashboard **Layer**) are listed in [NAMING.md](NAMING.md).

## The app

| Term | Meaning | In this lab |
|---|---|---|
| Observability | Seeing what hosts are doing from the data they emit, rather than logging in to each one. | Health samples land in MariaDB and show on Grafana. |
| Ingest | An endpoint that accepts data from elsewhere and stores it. | FastAPI `POST /ingest`. |
| FastAPI | Python web framework for HTTP APIs. | The `ingest` service on port 8080. |
| Payload | The JSON body of a request. | `host`, `cpu_pct`, `mem_pct`, `ok`. Sample host is `navi-01`. |
| MariaDB | A SQL database (MySQL-compatible). | Database `wired`, table `health_events`. |
| Grafana | Dashboards over a database or metrics store. | Dashboard **Layer** (anonymous viewer in the lab). |

## Containers and CI

| Term | Meaning | In this lab |
|---|---|---|
| LXC | A Linux container that behaves like a small VM: its own OS userland, not a single app process. | Where you run this lab so the workstation host stays clean. |
| Container (Docker) | A packaged process with its own filesystem, not a full VM. | `ingest`, `mariadb`, and `grafana` once Compose is up. These run *inside* the LXC. |
| Image | The immutable template a container is created from. | Built from `ingest/Dockerfile`; published to GHCR. |
| Registry | A store for container images. | GHCR: `ghcr.io/mciciriello/fleet-health-ingest`. |
| Docker Compose | A YAML file that starts several containers together. | `docker-compose.yml`, project name `wired`. |
| CI | Continuous integration: tests and builds on every push, not only on a laptop. | GitHub Actions workflow `ci`. |
| GitHub Actions | GitHub's CI runner. | Pytest, then build and push the image on `main`. |
| GHCR | GitHub Container Registry. | Where the ingest image is pushed. |

## AWS delivery

| Term | Meaning | In this lab |
|---|---|---|
| AWS | Amazon Web Services. A public cloud: rent compute, network, and storage instead of a box in a rack. | The target for the next deploy. Not running yet. |
| Terraform | Infrastructure as code: you declare cloud resources in files, then create or destroy them as a set. | Next. Estate prefix `wired`. |
| VPC | Virtual Private Cloud. Your own private network inside AWS. Linux analogue: the LAN you put servers on. | Later: `wired` VPC. |
| Subnet | A slice of a VPC's address space (often public vs private). | Later, with the VPC. |
| IAM | Identity and Access Management. Who (user, role, or service) is allowed to do what. | Later. Console user now; task role and GitHub role with Terraform. |
| S3 | Object storage. Files in buckets, not a POSIX filesystem. | Later: Terraform state or artifacts. |
| EC2 | A rented virtual machine. | Fallback if Fargate is a poor fit: one EC2 instead of ECS. |
| ECS | Elastic Container Service. Runs Docker images on AWS. | Preferred compute for `ingest`. |
| Fargate | ECS mode where AWS runs the containers; you do not manage the VMs underneath. | Preferred ECS launch type. |
| ALB | Application Load Balancer. HTTP reverse proxy in front of the app. Linux analogue: Caddy or nginx in front of a port. | Later, in front of ingest (and Grafana if it is exposed). |
| CloudWatch | AWS logs and metrics. | Later: container logs. |
| OIDC | OpenID Connect. One system proves who it is to another without a long-lived password. | Later: GitHub Actions assumes an AWS IAM role named from `protocol7`. No access keys in git. |
