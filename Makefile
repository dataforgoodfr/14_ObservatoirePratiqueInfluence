
build-api:
	@docker build opi-api -f opi-api/Dockerfile -t opi-api

up: build-api
	@docker compose -f docker-compose.yml -p opi up

down:
	@COMPOSE_PROJECT_NAME=opi docker compose down --remove-orphans
