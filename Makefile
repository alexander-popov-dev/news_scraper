COMPOSE = docker compose -f deploy/scraper/docker-compose.yaml

.PHONY: up-prod up-dev down-prod down-dev logs-prod logs-dev

up-prod:
	$(COMPOSE) --env-file .env up -d

up-dev:
	$(COMPOSE) --env-file .env.dev -p news-scraper-dev --env-file .env.dev up -d

down-prod:
	$(COMPOSE) --env-file .env down --rmi all

down-dev:
	$(COMPOSE) --env-file .env.dev -p news-scraper-dev down --rmi all

logs-prod:
	$(COMPOSE) --env-file .env logs -f --tail 10000

logs-dev:
	$(COMPOSE) --env-file .env.dev -p news-scraper-dev logs -f --tail 10000