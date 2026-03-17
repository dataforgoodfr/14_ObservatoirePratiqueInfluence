build-frontend:
	@docker build frontend -f frontend/Dockerfile -t opi-frontend

build-api:
	@docker build opi-api -f opi-api/Dockerfile -t opi-api

up: build-api build-frontend
	@docker compose -f docker-compose.yml -p opi up

down:
	@COMPOSE_PROJECT_NAME=opi docker compose down --remove-orphans


generate-python-api-client:
	wget http://localhost:8000/openapi.json -O openapi.json
	pipx run openapi-generator-cli[jdk4py] generate \
		-i openapi.json \
		-g python \
		-o ./data-extractors/src/ \
		--global-property=apiDocs=false,modelDocs=false,apiTests=false,modelTests=false \
		--additional-properties=generateSourceCodeOnly=true,packageName=api_client
	rm openapi.json
