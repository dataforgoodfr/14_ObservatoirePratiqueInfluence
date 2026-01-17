
build-api:
	@docker build opi-api -f opi-api/Dockerfile

up: build-api
	@docker compose -f docker-compose.yml -p opi up -d

down:
	@COMPOSE_PROJECT_NAME=opi docker compose down --remove-orphans
