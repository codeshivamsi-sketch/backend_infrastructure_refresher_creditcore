# CreditCore

A hands-on refresher on backend engineering: async APIs, microservices, event-driven architecture, and containerisation, built around a trivial lending domain.

## Tech Stack

- **FastAPI** — REST API framework
- **PostgreSQL** — primary database
- **SQLAlchemy + Alembic** — ORM and migrations
- **Redis + Celery** — async background jobs
- **Kafka** — event publishing and consumption
- **structlog** — structured JSON logging
- **Prometheus** — metrics scraping
- **Grafana** — metrics visualisation
- **Docker** — containerised infrastructure

## Services

- **Origination** (port 8000) — loan application lifecycle, idempotency, credit check jobs
- **Ledger** (port 8001) — double-entry bookkeeping for financial records

## Architecture

```
Client → Origination Service → PostgreSQL
                             → Redis (Celery background jobs)
                             → Kafka (loan.submitted events)
                             → Ledger Service → PostgreSQL

Prometheus → scrapes /metrics from Origination + Ledger
Grafana    → visualises metrics from Prometheus
```

## Running Locally

### Prerequisites
- Docker + Docker Compose
- make

### Start everything

```bash
make up
```

### Run migrations

```bash
# Origination
cd services/origination
alembic upgrade head

# Ledger
cd services/ledger
alembic upgrade head
```

### Run tests

```bash
cd services/origination
pytest tests/ -v
```

## API Endpoints

### Origination Service

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/applications` | Create loan application |
| GET | `/applications/{id}` | Get application by ID |
| PATCH | `/applications/{id}/submit` | Submit application |
| GET | `/tasks/{task_id}` | Check credit check job status |
| GET | `/health` | Health check |

## Observability

Prometheus and Grafana are included in the Docker setup.

| Service | URL |
|---------|-----|
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

Both services expose a `/metrics` endpoint scraped by Prometheus every 15s. Open Grafana, add Prometheus as a datasource (`http://prometheus:9090`), and build dashboards using metrics like `http_requests_total` and `http_request_duration_seconds_bucket`.
