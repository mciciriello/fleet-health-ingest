# Naming

Closed set. Do not invent new tokens. Product names (repo, GHCR image, FastAPI title, table `health_events`, HTTP paths) stay as they are.

| Token | Use |
|---|---|
| `wired` | Compose project name. MariaDB database. Later: AWS estate / VPC prefix. |
| `navi` | Reporting hosts: `navi-01`, then `navi-02` if needed. |
| `layer` | Grafana dashboard title, uid, and URL slug (`/d/layer/layer`). |
| `protocol7` | Reserved. Later: OIDC / GitHub-to-AWS IAM names only. |

Examples:

- Database: `wired.health_events`
- Sample POST host: `navi-01`
- Grafana datasource uid: `wired-mariadb`
- Later VPC: `wired` (not a new word)
