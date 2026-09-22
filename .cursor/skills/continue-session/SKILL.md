---
name: continue-session
description: Resume fleet-health-ingest from STATUS.md, teach AWS from a Linux-ops baseline, stay in scope, and update the handoff when the session ends. Use when starting a session, continuing this lab, explaining cloud terms, or when the user asks what is next.
---

# Continue session

Git-tracked handoff for this repo. Clone is enough. Do not look for a home-directory skill.

This lab is **for learning**. Do the work, and teach while doing it. The reader already knows Linux servers, LXC, Grafana, and MariaDB. AWS is a new lexicon for jobs they already do. Hold their hand. Do not assume prior AWS.

## Start

1. Read [AGENTS.md](../../../AGENTS.md), [STATUS.md](../../../STATUS.md), [NAMING.md](../../../NAMING.md), and [GLOSSARY.md](../../../GLOSSARY.md).
2. Take the first item under **Next** in STATUS. That is the work.
3. Do not add Kubernetes, a second cloud, vendor protocols, or host-side installs.
4. Hosts and cloud resources use only tokens in NAMING.md. Do not invent new ones.

## Teach

When a cloud term appears, always in this order:

1. The Linux / ops job they already know
2. The AWS (or Terraform / Actions) name
3. What it is **in this lab** (`wired`, `navi-01`, **Layer**, later `protocol7`)

Do not dump a lecture. One new word at a time when walking through a step. Point at GLOSSARY.md; if a term will stick, add it there.

| They already know | Cloud name |
|---|---|
| LAN you draw before you rack | VPC |
| VLAN / address slice | subnet |
| `/etc/passwd` + sudoers, including service users | IAM |
| Fileserver share, not ext4 | S3 |
| A VM | EC2 |
| `docker compose up` without SSH to the box | ECS; Fargate = you do not manage the VM under it |
| Caddy / nginx in front of the app | ALB |
| `journalctl`, shipped off the box | CloudWatch logs |
| Kickstart / Ansible you wish you had written first | Terraform |
| CI proves who it is; no root password in a drawer | OIDC from GitHub Actions |

## Constraints

- Public repo: no personal details, employer names, internal product names, customer data, secrets.
- Runtime is the LXC lab. Docker Engine is assumed **inside** that container. Do not pollute the host.
- Keep changes proportional. This is one ingest pipeline plus its delivery layer.

## End

Rewrite the **Last session** block in `STATUS.md`:

- Date
- What landed (files or proof, not a diary)
- What is still **Next**
- **Blockers** if any

If the next step is now done, move it to **Done** and promote the following item.
