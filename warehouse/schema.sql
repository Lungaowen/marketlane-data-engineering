CREATE SCHEMA IF NOT EXISTS warehouse;

CREATE TABLE IF NOT EXISTS raw_events (
    id BIGSERIAL PRIMARY KEY,
    event_type TEXT NOT NULL,
    payload JSONB NOT NULL,
    received_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS warehouse.fact_bookings (
    booking_id TEXT PRIMARY KEY,
    vendor_id TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    amount NUMERIC(14, 2) NOT NULL CHECK (amount >= 0),
    created_at TIMESTAMPTZ NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_fact_bookings_vendor
    ON warehouse.fact_bookings (vendor_id);

CREATE INDEX IF NOT EXISTS idx_fact_bookings_created_at
    ON warehouse.fact_bookings (created_at);

CREATE OR REPLACE VIEW warehouse.booking_daily_summary AS
SELECT
    DATE(created_at) AS booking_date,
    COUNT(*) AS booking_count,
    SUM(amount) AS total_amount,
    AVG(amount) AS average_amount
FROM warehouse.fact_bookings
GROUP BY DATE(created_at);
