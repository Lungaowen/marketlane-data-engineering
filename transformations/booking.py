from events.contracts import BookingCreated


def to_fact_booking(event: BookingCreated) -> dict:
    return {
        "booking_id": event.booking_id,
        "vendor_id": event.vendor_id,
        "customer_id": event.customer_id,
        "amount": event.amount,
        "created_at": event.created_at,
    }
