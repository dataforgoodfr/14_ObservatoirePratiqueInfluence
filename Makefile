build-frontend:
	@docker build frontend -f frontend/Dockerfile -t opi-frontend

build-api:
	@docker build opi-api -f opi-api/Dockerfile -t opi-api

up: build-api build-frontend
	@docker compose -f docker-compose.yml -p opi up

down:
	@COMPOSE_PROJECT_NAME=opi docker compose down --remove-orphans
