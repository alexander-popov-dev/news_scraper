COMPOSE = docker compose -f deploy/scraper/docker-compose.yaml
COMPOSE_PROD = $(COMPOSE) --env-file .env
COMPOSE_DEV = APP_ENV_FILE=.env.dev $(COMPOSE) --env-file .env.dev -p news-scraper-dev

.PHONY: up-prod up-dev down-prod down-dev logs-prod logs-dev

up-prod:
	$(COMPOSE_PROD) up -d

up-dev:
	$(COMPOSE_DEV) up -d

down-prod:
	$(COMPOSE_PROD) down --rmi all

down-dev:
	$(COMPOSE_DEV) down --rmi all

logs-prod:
	$(COMPOSE_PROD) logs -f --tail 10000

logs-dev:
	$(COMPOSE_DEV) logs -f --tail 10000