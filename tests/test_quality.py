import pytest
from pydantic import ValidationError

from data_quality.rules import validate_booking


def test_negative_booking_amount_is_rejected():
    with pytest.raises(ValidationError):
        validate_booking({
            "event": "booking.created",
            "bookingId": "b-1",
            "vendorId": "v-1",
            "customerId": "c-1",
            "amount": -1,
            "createdAt": "2026-09-18T10:30:00Z",
        })
