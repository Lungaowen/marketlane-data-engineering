# 🟢 Marketlane Data Engineering

A data-engineering platform for Marketlane that consumes backend events, validates and transforms them, and loads analytics-ready data into **ClickHouse**, a dedicated analytical database.

## Architecture

```text
Marketlane Services
       │
       │ domain events
       ▼
 RabbitMQ / Event Broker
       │
       ▼
 Python Event Consumer
       │
       ├── raw_events
       │
       ▼
 Validation + Transformation
       │
       ▼
 ClickHouse Analytical Database
       │
       ├── raw events
       ├── fact tables
       └── analytical views
              │
              ▼
 Analytics Service / Power BI / AI
```

## Why ClickHouse?

ClickHouse is the analytical store for this platform. It is deliberately separate from Marketlane's transactional databases such as Supabase/PostgreSQL.

- **Supabase/PostgreSQL:** system of record for application transactions.
- **RabbitMQ:** transports domain events from Marketlane services.
- **ClickHouse:** stores analytics-oriented event and fact data for fast aggregation and reporting.
- **Analytics Service / Power BI / AI:** consumes analytical datasets without putting reporting load on transactional services.

This separation gives the application and analytics workloads different storage paths and scaling characteristics.

## V1 scope

- Consume Marketlane events from RabbitMQ.
- Persist original events in ClickHouse for traceability.
- Validate supported event contracts.
- Transform `booking.created` events into a ClickHouse fact table.
- Expose an analytics-ready daily booking summary view.
- Run the complete pipeline locally with Docker Compose.
- Provide automated tests and CI validation.

## Project structure

```text
ingestion/       RabbitMQ connection and event consumers
events/          Event contracts and validation
transformations/ Domain-to-analytics transformations
warehouse/       ClickHouse schema and analytical views
data_quality/    Data validation rules
scripts/         Local event producer and pipeline helpers
tests/           Unit tests
.github/         CI workflow
```

## Run locally

Requirements: Docker and Docker Compose.

```bash
docker compose up --build
```

Publish a sample event from another terminal:

```bash
docker compose run --rm producer
```

ClickHouse is available through:

- HTTP: `http://localhost:8123`
- Native protocol: `localhost:9000`
- Database: `warehouse`
- User: `marketlane`

The analytical schema is initialized from `warehouse/schema.sql`.

## Example analytical query

```sql
SELECT *
FROM warehouse.booking_daily_summary
ORDER BY booking_date DESC;
```

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

Marketlane services remain the owners of transactional data. This repository creates analytical representations from events; it does not become the system of record for bookings.

## Next evolution

- Add payment, vendor, marketplace, and other domain-event consumers.
- Add event IDs and stronger idempotency across all event types.
- Add data-quality gates and lineage metadata.
- Introduce dbt for larger transformation models when the analytical layer grows.
- Add orchestration when pipelines become scheduled and multi-stage.
- Add object storage/lake ingestion for large historical datasets when needed.
- Connect an analytics service, Power BI, and AI workloads to ClickHouse.
- Add production ClickHouse Cloud or self-hosted deployment configuration separately from local Docker development.
