# Data Extraction API Backend

REST API for centralized extraction task management and social media data ingestion. Built with [FastAPI](https://fastapi.tiangolo.com/).

Part of the **Observatoire des Pratiques d'Influence** project. See [../README.md](../README.md) for monorepo context.

## Architecture

The API sits between data extractors (workers scraping YouTube, TikTok, Instagram) and a [NocoDB](https://nocodb.com/) database:

```
Extractors → opi-api (task queue + ingestion) → NocoDB + PostgreSQL
```

- **PostgreSQL** — stores the extraction task queue
- **NocoDB** — serves as the primary data store for social media accounts and posts (upserted via its REST API)
- **asyncpg** — async PostgreSQL connection pool
- **golang-migrate** — database schema migrations

## Setup

### Prerequisites

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) (package manager)
- PostgreSQL database
- NocoDB instance

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `POSTGRES_DSN` | `postgresql://postgres:postgres@localhost:5432/opidb` | PostgreSQL connection string |
| `ASYNCPG_MIN_POOL_SIZE` | `1` | Minimum pool connections |
| `ASYNCPG_MAX_POOL_SIZE` | `1` | Maximum pool connections |
| `API_KEY` | — | Bearer token for endpoint authentication |
| `NOCODB_URL` | — | Base URL of the NocoDB instance |
| `NOCODB_API_TOKEN` | — | API token for NocoDB authentication |
| `NOCODB_BASE_ID` | — | NocoDB base/workspace ID |
| `NOCODB_ACCOUNT_TABLE` | `Account` | NocoDB table name for accounts |
| `NOCODB_POST_TABLE` | `Post` | NocoDB table name for posts |

### Run with docker

```bash
docker build -t opi-api .
docker run -e POSTGRES_DSN="..." -e API_KEY="..." -e NOCODB_URL="..." ... opi-api
```

## API Endpoints

All endpoints require `Authorization: Bearer <api_key>` unless noted.

### Health

| Method | Path | Description |
|---|---|---|
| `GET` | `/ping` | Health check (returns `"pong"`) (no auth) |

### Extraction Tasks — Task Queue Management

| Method | Path | Description |
|---|---|---|
| `POST` | `/extraction-task/` | Register new extraction tasks |
| `POST` | `/extraction-task/acquire` | Acquire an available task (240 min lease) |
| `POST` | `/extraction-task/{task_uid}/mark-completed` | Mark task as COMPLETED |
| `POST` | `/extraction-task/{task_uid}/mark-failed/` | Mark task as FAILED (body: `{"error": "..."}`) |
| `POST` | `/extraction-task/recycle-failed` | Recycle FAILED tasks back to AVAILABLE |
| `POST` | `/extraction-task/recycle-expired` | Recycle expired ACQUIRED tasks back to AVAILABLE |
| `GET` | `/extraction-task/stats` | Task statistics (filterable by social_network, account_id, task_type) |

### Social Network Data — NocoDB Ingestion

| Method | Path | Description |
|---|---|---|
| `POST` | `/accounts/` | Upsert accounts into NocoDB |
| `POST` | `/posts/` | Upsert posts into NocoDB |

## Task Lifecycle

1. **Registration** — tasks created with status `AVAILABLE`
2. **Acquisition** — worker acquires a task → status becomes `ACQUIRED` with 240 min `visible_at` lease
3. **Processing** — worker extracts data according to task config
4. **Completion / Failure** — worker marks task as `COMPLETED` or `FAILED` (with error message)
5. **Recycling** — failed/expired tasks can be recycled back to `AVAILABLE`

### Task Types

| Type | Config |
|---|---|
| `extract-account` | `account_id` |
| `extract-post-list` | `account_id`, `published_after`, `published_before` |
| `extract-post-details` | `account_id`, `post_id` |

### Social Networks

`youtube`, `tiktok`, `instagram`

## Database (PostgreSQL)

Schema: `v1`. Key tables: `extraction_task`.

Migrations are in [`migrations/`](./migrations/) and use [golang-migrate](https://github.com/golang-migrate/migrate) format.
Migrations are run in docker entrypoint.

## Development

```bash
# Install dependencies
uv sync

# Type checking
uv run mypy src/app

# Linting
uv run ruff check src/app

# Formatting
uv run ruff format src/app
```
