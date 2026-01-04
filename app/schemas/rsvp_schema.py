from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class RSVP(BaseModel):
    name: Optional[str] = None
    email: EmailStr

    class Config:
        orm_mode = True

class RSVPCreate(RSVP):
    pass


class RSVPRead(RSVP):
    id: int
    is_active: bool
    is_superuser: bool

    model_config = ConfigDict(from_attributes=True)