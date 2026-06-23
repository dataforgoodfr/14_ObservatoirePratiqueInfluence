# Observatoire des pratiques d'influence

This repository contains the code that allowed to build the data and content of the Observatoire des pratiques d'influence website.

The project is split into four functional parts, most of which live in this repository:

- _Data Extraction Code_ for extracting Social Network posts: This relies on 2 sub projects:
- _Data Extractors_ (see [./data-extractors/README.md](./data-extractors/README.md)) a long running Python CLI that fetches posts from the three supported social networks. It can read tasks and store results either on the local filesystem or in a shared backend (see below).
- _Data Extraction API Backend_ (see [./opi-api/README.md](./opi-api/README.md)) a Python FastAPI server that centralises task definitions, acquisition, and result storage, letting extraction jobs be distributed across multiple machines.
- _Brand annotation_: Identifies brands that paid influencers for specific posts.
- _Data analysis and reporting_: Metabase is used for dashboards and reports.
- _Web site_: [./frontend/README.md](./frontend/README.md) nextjs public website exposing some Metabase dashboards.

# Architecture

For a list of all technical components, general data flow and data model see [./docs/architecture.md](./docs/architecture.md).

# Running things locally

## Running the *Web Site*

See  [./frontend/README.md](./frontend/README.md)


## Running the *Data extraction Api Backend* using docker compose

A docker compose exists that starts:
- The Data Extraction API Backend see [./opi-api/README.md](./opi-api/README.md)
- A local NocoDB used to store extraction results
- A postgres used for 2 things:
  - The NocoDB storage
  - The data extraction api backend extraction tasks storage

### One time manual setup required for Data extraction api backend

- Start the docker compose (see below)
- Connect to Noco UI
- Use UI to define a Noco API token
- Create a new Noco base and copy the base id (or copy the id of the default base)
- Run the Noco tables creation script [./noco_setup/create-noco-tables.sh](./noco_setup/create-noco-tables.sh) providing the base id and API Token created before
- Modify docker-compose `opi-api` service > environnement values to use the correct values for NOCODB_API_TOKEN & NOCODB_BASE_ID

### Running docker compose

The build and start of docker-compose is wrapped in a make target:
When running `make up`:
- Extraction API Backend doc is available at `http://localhost:8000/docs#`

## Running data extraction

See [./data-extractors/README.md](./data-extractors/README.md)

## Running brand annotation

See [./brand-annotation/README.md](./brand-annotation/README.md)

# Deployment Environment

Staging environment current setup:
* _NocoDB_ base is hosted in D4G shared NocoDB
* _Metabase_ runs on coolify deployed using predefined coolify service Metabase 
* _Data Extraction API Backend_ runs on coolify and is re-deployed from `/opi-api/Dockerfile`on each commit to `main`
* Postgres db for _Data Extraction API Backend_ runs on coolify
* Website is deployed on github pages on each commit to `main` and is available on subdomain observatoire.payetoninfluence.org (subdomain managed by Amélie on OVH)
