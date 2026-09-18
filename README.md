# 📊 Marketlane Data Engineering

A data-engineering platform for Marketlane that consumes backend events, validates and transforms them, and loads analytics-ready data into a warehouse-style PostgreSQL database.

## Architecture

```
Marketlane Services
       │
       │ domain events
       ▼
 RabbitMQ / Event Broker
       │
       ▼
 Python Event Consumers
       │
       ├── raw_events
       │
       ▼
 Validation + Transformation
       │
       ▼
 PostgreSQL Warehouse
       │
       ├── staging
       ├── warehouse
       └── analytics
              │
              ▼
 Analytics Service / Power BI / AI
```

## V1 scope

- Consume Marketlane events from RabbitMQ.
- Persist the original event for traceability.
- Validate supported event contracts.
- Transform `booking.created` events into an analytics fact table.
- Expose an analytics-ready SQL view.
- Run the whole pipeline locally with Docker Compose.
- Provide automated tests and CI validation.

## Project structure

```
ingestion/        RabbitMQ connection and event consumers
events/           Event contracts and validation
transformations/ Domain-to-warehouse transformations
warehouse/        PostgreSQL schema and analytics views
data_quality/     Data validation rules
scripts/          Local producer and pipeline helpers
tests/            Unit tests
.github/          CI
```

## Run locally

Requirements: Docker and Docker Compose.

```bash
docker compose up --build
```

In another terminal, publish a sample booking event:

```bash
docker compose run --rm producer
```

The consumer stores the raw event and loads `warehouse.fact_bookings`.

## Local services

| Service | Purpose | Port |
|---|---|---:|
| `rabbitmq` | Event broker | 5672 / 15672 |
| `warehouse` | PostgreSQL analytical store | 5432 |
| `consumer` | Event ingestion pipeline | — |
| `producer` | Local demo event publisher | — |

## Event contract

The first supported event is:

```json
{
  "event": "booking.created",
  "bookingId": "booking-001",
  "vendorId": "vendor-001",
  "customerId": "customer-001",
  "amount": 350.0,
  "createdAt": "2026-09-18T10:30:00Z"
}
```

The production Marketlane services remain the owners of transactional data. This repository consumes events and creates analytical representations; it does not become the system of record for bookings.

## Next evolution

- Add payment, vendor and marketplace event consumers.
- Add CDC for selected database sources where events are insufficient.
- Introduce dbt for larger transformation models.
- Add orchestration when pipelines become scheduled and multi-stage.
- Move from local PostgreSQL to a managed warehouse when scale requires it.
- Add data lineage, observability and stronger data-quality gates.
