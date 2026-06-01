
# Data extractors CLI

This python CLI allows to extract posts and accounts from supported social networks (tiktok, instagram, youtube).

It can be used with 2 different task and result backends depending on use case:
* The `filesystem backend` is mostly for testing or single machine extraction.
* The `Data Extraction API Backend` allows to share and distributes a pool of extraction tasks across multiple machines for parallel execution

# Using CLI with filesystem backend

## Usage flow

1. Configure the CLI to use the file system backend by configuring .env file [see below](#env-config-for-file-system-backend).
2. Define tasks to extract: 
    * either using the `generate-task` CLI sub-command ([see doc below](#generate-task-sub-command)).
    * or manually editing [./data/extraction-tasks.csv] ([see file format doc below](#extraction-taskscsv)).
3. Run the extraction using the `extract` CLI sub-command ([see doc below](#extract-sub-command)).
4. Use data from local [./data/results/accounts.csv] and [./data/results/posts.csv]
5. Optionally upload the data from [./data/results/accounts.csv] and [./data/results/posts.csv] to a NocoDB using `upload-results` sub-command (see reference doc below)


## .env config for file system backend

*Note* see extract sub-command reference doc below for social network specific settings

```ini
# Configure extract sub-command to use file system backend
BACKEND=fs

# Optional: Only needed if using generate-task sub-command 
# Configure generate-task sub-command to use file system backend
GENERATE_TASK_BACKEND=fs

# Optional: Only needed if using upload-results sub-command 
# Configure target Noco Db
UPLOAD_NOCODB_API_TOKEN=<Obtained from NocoDB Account settings see https://nocodb.com/docs/product-docs/account-settings/api-tokens>
UPLOAD_NOCODB_URL=<Noco DB Url>
UPLOAD_NOCODB_BASE_ID=<Base id in which table should exist>
UPLOAD_NOCODB_ACCOUNT_TABLE_NAME=<Account Table Name>
UPLOAD_NOCODB_POST_TABLE_NAME=<Post Table Name>
```


# Using CLI with Data Extraction API Backend

## Usage flow

1. Configure the CLI to use the Data Extraction API Backend by configuring .env file ([see below](#env-config-for-data-extraction-api-backend))
2. Define tasks to extract: 
    * *Note:* In a distributed setup this is needed only once as task pool is stored in the central server and so is shared between machines running the extract CLI
    * Either using the `generate-task` CLI sub-command ([see doc below](#generate-task-sub-command)). 
    * Or using the API endpoint `/extraction-task/` directly.
3. Run the extraction using the `extract` CLI sub-command ([see doc below](#extract-sub-command)).
4. Use accounts and posts data from the NocoDB tables to which backend pushed 


## .env config for Data Extraction API backend

*Note* see extract sub-command reference doc below for social network specific settings
```ini
# Configure extract sub-command to use API Backend
BACKEND=api
API_URL=<backend base url>
API_KEY=<Token matching the env API_KEY used when starting backend API server>

# Optional: Only needed if using generate-task sub-command 
# Configure generate-task sub-command to use API backend
GENERATE_TASK_BACKEND=api
GENERATE_TASK_API_URL=<backend base url>
GENERATE_TASK_API_KEY=<Token matching the env API_KEY used when starting backend API server>

```

# CLI Reference documentation

The CLI is composed of 3 commands:
* extract
* generate-task
* upload-results:

CLI can be run using `uv run src/main.py <subcommand>`

## Prerequisites
* Clone repository
* [uv](https://docs.astral.sh/uv/getting-started/installation/)
* run `uv sync` in repository data-extractors folder
* Optional: If using the *Data Extraction API Backend* the server needs to be started somewhere (see dedicated doc [../opi-api/README.md])

## Commands

### extract sub-command
This command starts a long running process that:
* polls backend for available tasks every 10 seconds
* if any available acquire and executes the task
* store result and mark task a completed

General config
- `-n` / `--social-network` / env: `SOCIAL_NETWORK` — social network to extract. Choices: `youtube`, `tiktok`, `instagram`. Default: `youtube`.
- `--task-polling-interval` / env: `TASK_POLLING_INTERVAL` — seconds between task polling. Default: `10`.
- `--cache-folder` / env: `CACHE_FOLDER` — cache folder path. Default: `data/.cache`.
- `--cache-ttl-seconds` / env: `CACHE_TTL_SECONDS` — cache TTL in seconds. Default: `604800` (7 days).
- `--exit-after-task-failure` / env: `EXIT_AFTER_TASK_FAILURE` — exit after failure. `true` (immediate), `false` (never), or an integer count. Default: `true`.
- `--backend` / env: `BACKEND` — task/result backend. Choices: `fs`, `api`. Default: `api`.
- `--api-url` / env: `API_URL` — API backend base URL. Default: `http://localhost:8000`.
- `--api-key` / env: `API_KEY` — API auth token (required when backend is `api`).
- `--fs-tasks-file` / env: `FS_TASKS_FILE` — tasks CSV path for filesystem backend. Default: `data/extraction_tasks.csv`.
- `--fs-result-folder` / env: `FS_RESULT_FOLDER` — result folder for filesystem backend. Default: `data/results`.

#### Youtube

Uses the [YouTube Data API v3](https://developers.google.com/youtube/v3).

Required config:
- `--youtube__api-key` / env: `YOUTUBE__API_KEY` — YouTube Data API v3 key.

Account IDs can be either a channel ID (e.g. `UC...`) or a handle (starting with `@`).  
Supports account extraction, post list extraction (with date filtering), and post detail extraction.

#### Tiktok

Two implementations are available, controlled by `--tiktok__implementation` / `TIKTOK__IMPLEMENTATION`:

- **`TTA`** (default) — Uses the [TikTokApi](https://github.com/davidteather/TikTok-Api) library with Playwright for `ms_token` acquisition. Requires `playwright install chromium`.
- **`V1`** — Legacy & incomplete web scraping via requests + BeautifulSoup. No dependencies beyond requests. `extract-post-list` is not supported.

TTA-specific options:
- `--tiktok__ms-token` / env: `TIKTOK__MS_TOKEN` — How to obtain the `ms_token`: set to `PLAYWRIGHT` to auto-fetch from `tiktok.com/explore`, or provide a literal token string.
- `--tiktok__headless` / env: `TIKTOK__HEADLESS` — Run Playwright browser in headless mode. Default: `true`.
- `--tiktok__store-raw-data` / env: `TIKTOK__STORE_RAW_DATA` — Save raw API responses to disk. Default: `false`.

#### Instagram

Uses the [instaloader](https://instaloader.github.io/) library. No additional config or env vars required.

*Note:* Instagram often rejects scraping from non-mobile connections.  
Connect your PC to internet through your phone mobile connection using a hotspot. Ensure wifi is disabled on the phone otherwise this is useless.

Instagram extraction supports account extraction (profile info, followers, followees), post list extraction (with date filtering, pinned posts handled), and post detail extraction (includes sponsor/brand detection via `is_sponsored`).


### generate-task sub-command

Reads a CSV of account URLs and generates extraction tasks, storing them to either the filesystem or the API backend.

Input file format ([`data/account_urls.csv`] by default):
```csv
Account Url
https://www.instagram.com/nabilla
https://www.tiktok.com/@tiboinshape
https://www.youtube.com/channel/UCWeg2Pkate69NFdBeuRFTAw
```

For each URL, the command detects the social network from the URL and creates tasks (either `extract-account`, `extract-post-list`, or both).

Options:
- `--task-type` / env: `GENERATE_TASK_TASK_TYPE` — which task types to generate. Choices: `all`, `account`, `post-list`. Default: `all`.
- `--published-after` / env: `GENERATE_TASK_PUBLISHED_AFTER` — start date for post-list tasks (ISO 8601). Default: `2025-01-01T00:00:00+00:00`.
- `--published-before` / env: `GENERATE_TASK_PUBLISHED_BEFORE` — end date for post-list tasks (ISO 8601). Default: `2026-01-01T00:00:00+00:00`.
- `--urls-file` / env: `GENERATE_TASK_URLS_FILE` — input CSV with account URLs. Default: `data/account_urls.csv`.
- `--backend` / env: `GENERATE_TASK_BACKEND` — where to store generated tasks. Choices: `fs`, `api`. Default: `fs`.
- `--api-url` / env: `GENERATE_TASK_API_URL` — API URL (if backend=`api`). Default: `http://localhost:8000`.
- `--api-key` / env: `GENERATE_TASK_API_KEY` — API token (if backend=`api`).
- `--fs-replace` / env: `GENERATE_TASK_FS_REPLACE` — replace or append to existing tasks CSV. Default: `false`.
- `--fs-tasks-file` / env: `GENERATE_TASK_FS_TASKS_FILE` — output tasks CSV path. Default: `data/extraction_tasks.csv`.

### upload-results sub-command

*Note:* This command is only relevant when using the filesystem backend.

Uploads locally stored `accounts.csv` and `posts.csv` to NocoDB tables using upsert semantics (creates new records, updates existing ones by matching key fields).

Required config:
- `--nocodb-url` / env: `UPLOAD_NOCODB_URL` — NocoDB server URL.
- `--nocodb-base-id` / env: `UPLOAD_NOCODB_BASE_ID` — NocoDB base ID.
- `--nocodb-api-token` / env: `UPLOAD_NOCODB_API_TOKEN` — API token (obtained from NocoDB Account Settings, see [NocoDB docs](https://nocodb.com/docs/product-docs/account-settings/api-tokens)).
- `--nocodb-account-table-name` / env: `UPLOAD_NOCODB_ACCOUNT_TABLE_NAME` — NocoDB account table name.
- `--nocodb-post-table-name` / env: `UPLOAD_NOCODB_POST_TABLE_NAME` — NocoDB post table name.

Optional:
- `--result-folder` / env: `UPLOAD_RESULT_FOLDER` — result folder path. Default: `data/results`.
- `--accounts-csv` / env: `UPLOAD_ACCOUNTS_CSV` — accounts CSV path. Default: `data/results/accounts.csv`.
- `--posts-csv` / env: `UPLOAD_POSTS_CSV` — posts CSV path. Default: `data/results/posts.csv`.
- `--accounts-skip-rows` / env: `UPLOAD_ACCOUNTS_SKIP_ROWS` — skip N rows from accounts CSV. Default: `0`.
- `--posts-skip-rows` / env: `UPLOAD_POSTS_SKIP_ROWS` — skip N rows from posts CSV. Default: `0`.
- `--nocodb-account-field-name` / env: `UPLOAD_NOCODB_ACCOUNT_FIELD_NAME` — post table's link-to-account field name. Default: `Account`.


# File format for file system based storage

## accounts.csv

Stores extracted account data. Written to `data/results/accounts.csv` by default.

| Column | Type | Description |
|---|---|---|
| `social_network` | string | `youtube`, `tiktok`, or `instagram` |
| `account_id` | string | Account/channel ID or username |
| `account_extraction_date` | datetime (ISO) | When data was extracted |
| `handle` | string (nullable) | Display name / custom URL |
| `description` | string | Biography / channel description |
| `follower_count` | integer | Number of followers / subscribers |
| `following_count` | integer | Number of accounts this account follows |
| `post_count` | integer | Number of posts / videos |
| `view_count` | integer | Total view count |
| `like_count` | integer | Total like count |
| `categories` | string (comma-separated) | List of categories / topics |

## posts.csv

Stores extracted post data. Written to `data/results/posts.csv` by default.

| Column | Type | Description |
|---|---|---|
| `social_network` | string | `youtube`, `tiktok`, or `instagram` |
| `post_id` | string | Post / video ID |
| `account_id` | string | Owner account ID |
| `post_extraction_date` | datetime (ISO) | When data was extracted |
| `post_url` | string | URL to the post |
| `title` | string | Post title |
| `description` | string | Post description / caption |
| `comment_count` | integer | Number of comments |
| `view_count` | integer | Number of views |
| `repost_count` | integer | Number of reposts |
| `like_count` | integer | Number of likes |
| `share_count` | integer | Number of shares |
| `categories` | string (comma-separated) | Category / topic labels |
| `tags` | string (comma-separated) | Hashtags or channel tags |
| `sn_has_paid_placement` | boolean | Whether post is sponsored / an ad |
| `sn_brand` | string | Brand name (if sponsored) |
| `post_type` | string | Type of post (e.g. `video`, `GraphSidecar`) |
| `text_content` | string | Additional text content (e.g. tagged users) |

## extraction-tasks.csv

Stores extraction tasks for the filesystem backend. Written to `data/extraction_tasks.csv` by default.

| Column | Type | Description |
|---|---|---|
| `id` | uuid | Task unique identifier |
| `social_network` | string | `youtube`, `tiktok`, or `instagram` |
| `type` | string | `extract-account`, `extract-post-list`, or `extract-post-details` |
| `task_config` | string (JSON) | Task configuration (see below) |
| `status` | string | `AVAILABLE`, `ACQUIRED`, `COMPLETED`, or `FAILED` |
| `visible_at` | datetime (ISO) or empty | When an ACQUIRED task becomes visible again (timeout) |
| `error` | string or empty | Error message if FAILED |

`task_config` JSON structures:

For `extract-account`:
```json
{"account_id": "some_username_or_id"}
```
For `extract-post-list`:
```json
{"account_id": "some_username_or_id", "published_after": "2025-01-01T00:00:00+00:00", "published_before": "2026-01-01T00:00:00+00:00"}
```
For `extract-post-details`:
```json
{"account_id": "some_username_or_id", "post_id": "some_post_id"}
```


# Development


```bash
# Install dependencies
uv sync

# Type checking
uv run mypy src

# Linting
uv run ruff check src

# Formatting
uv run ruff format src

## Regenerating API client from Data Extraction API Backend OpenAPI 
# 1. Start Data Extraction API Backend locally (see [../opi-api/README.md])
# 2. then run make
make -C .. generate-python-api-client
```
