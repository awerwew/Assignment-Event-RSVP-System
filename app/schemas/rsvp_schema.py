from pydantic import BaseModel, EmailStr, ConfigDict



class RSVP(BaseModel):
    id: int
    name: str
    email: EmailStr
    event_id: int

    class Config:
        orm_mode = True

class RSVPCreate(BaseModel):
    name: str
    email: EmailStr
    


class RSVPRead(BaseModel):
    id: int
    is_active: bool
    is_superuser: bool

    model_config = ConfigDict(from_attributes=True)