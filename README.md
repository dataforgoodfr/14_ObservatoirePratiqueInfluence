This repository contains the frontend and API for the "Observatoire des pratiques d'influence" project.
It uses FastAPI for the API and NextJS/React for the frontend.

# Local development

You will need to have [docker](https://www.docker.com/) to run the local stack.

## Starting the stack

`make up`

The frontend will be available at `http://localhost:3000/` and the API doc is available at `http://localhost:8000/docs#`

## Building a specific image

- API: `make build-api`
- Frontend: `make build-frontend`
