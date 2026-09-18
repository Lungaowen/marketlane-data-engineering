from events.contracts import BookingCreated
from transformations.booking import to_fact_booking


def test_booking_event_transforms_to_fact():
    event = BookingCreated.model_validate({
        "event": "booking.created",
        "bookingId": "b-1",
        "vendorId": "v-1",
        "customerId": "c-1",
        "amount": 350,
        "createdAt": "2026-09-18T10:30:00Z",
    })

    fact = to_fact_booking(event)

    assert fact["booking_id"] == "b-1"
    assert fact["vendor_id"] == "v-1"
    assert fact["amount"] == 350
