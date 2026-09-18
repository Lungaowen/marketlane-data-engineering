from events.contracts import BookingCreated


def validate_booking(payload: dict) -> BookingCreated:
    return BookingCreated.model_validate(payload)
