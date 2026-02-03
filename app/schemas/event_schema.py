from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from app.schemas.rsvp_schema import RSVP






class EventCreate(BaseModel):
    title: str
    description: str
    date: date
    location: str
    flyer: Optional[str] = None



class EventOut(BaseModel):
    id: int
    title: str
    description: str
    date: str
    location: str
    flyer: Optional[str] = None
    rsvps: List[RSVP] = []

    class Config:
        orm_mode = True 