from pydantic import BaseModel
from typing import Optional, List
from app.schemas.rsvp_schema import RSVP



class Event(BaseModel):
    id: int
    title: str
    description: str
    date: str
    location: str
    flyer_filename: Optional[str] = None
    rsvps: List[RSVP] = []

    class Config:
        orm_mode = True


class EventCreate(BaseModel):
    title: str
    description: str
    date: str
    location: str
    flyer_filename: Optional[str] = None
