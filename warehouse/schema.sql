CREATE DATABASE IF NOT EXISTS warehouse;

CREATE TABLE IF NOT EXISTS warehouse.raw_events
(
    event_type String,
    payload String,
    received_at DateTime64(3, 'UTC') DEFAULT now64(3)
)
ENGINE = MergeTree
ORDER BY (received_at, event_type);

CREATE TABLE IF NOT EXISTS warehouse.fact_bookings
(
    booking_id String,
    vendor_id String,
    customer_id String,
    amount Decimal(18, 2),
    created_at DateTime64(3, 'UTC'),
    loaded_at DateTime64(3, 'UTC') DEFAULT now64(3)
)
ENGINE = ReplacingMergeTree(loaded_at)
ORDER BY booking_id;

CREATE VIEW IF NOT EXISTS warehouse.booking_daily_summary AS
SELECT
    toDate(created_at) AS booking_date,
    count() AS booking_count,
    sum(amount) AS total_amount,
    avg(amount) AS average_amount
FROM warehouse.fact_bookings FINAL
GROUP BY booking_date;
