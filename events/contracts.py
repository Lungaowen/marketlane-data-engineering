from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class BookingCreated(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    event: str = Field(pattern=r"^booking\.created$")
    booking_id: str = Field(alias="bookingId", min_length=1)
    vendor_id: str = Field(alias="vendorId", min_length=1)
    customer_id: str = Field(alias="customerId", min_length=1)
    amount: float = Field(ge=0)
    created_at: datetime = Field(alias="createdAt")
