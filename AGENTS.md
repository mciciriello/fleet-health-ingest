# Agent guide

Public observability ingest lab. Read this and [STATUS.md](STATUS.md) before changing anything.

## Start of session

1. Read [README.md](README.md) (why, pipeline, stack).
2. Read [STATUS.md](STATUS.md) (what is done, the next concrete step).
3. Read [NAMING.md](NAMING.md). Use only those tokens for hosts and resources. Do not invent new ones.
4. Do the next STATUS item. Do not invent a second project.

## Teach

This lab is for learning the cloud delivery layer from a Linux-ops baseline. The reader knows servers, LXC, Grafana, and MariaDB. AWS is new words for old jobs.

When a cloud term appears: Linux analogue first, then the AWS name, then what it is in this lab. One new word at a time. Use [GLOSSARY.md](GLOSSARY.md); add a row if the term will stick. Do not assume prior AWS.

## What this repo is

Generic host health: HTTP POST JSON to FastAPI, MariaDB store, Grafana read. Docker Compose locally. GitHub Actions for test and GHCR. Terraform on AWS is the remaining delivery layer.

It is not a vendor product clone. Payload is `host`, `cpu_pct`, `mem_pct`, `ok` only. Cloud terms: [GLOSSARY.md](GLOSSARY.md).

## Public repo hygiene

This repository is public. Do not add:

- Personal details, employer names, internal product names, customer data
- Long-lived cloud keys, `.pem` files, real passwords
- Career or keyword-gap framing (that lives outside this repo)

Lab Compose passwords are labelled as lab defaults. Do not reuse them on AWS.

Use a regular hyphen `-` in writing. Do not use em dashes.

## Runtime

Local work (Compose, venv, later AWS CLI / Terraform) runs **inside an LXC container**. Docker Engine must already be available there.

- Do not install Docker, Terraform, or AWS CLIs on the workstation host.
- Do not add a Proxmox CT template unless asked.

## End of session

Update [STATUS.md](STATUS.md): last session (date + what changed), done, next, blockers. Keep it short enough that a clone on another machine can continue.
