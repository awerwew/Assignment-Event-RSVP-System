

from datetime import date
from fastapi import APIRouter, Depends, Form, UploadFile, File
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.event import Event
from app.models.rsvp import RSVP
from app.api.deps import UPLOAD_DIR

#this sis trial
from app.models.user import User
from app.api.deps import get_current_active_user


router = APIRouter()





@router.post("/events/", status_code=201)
def create_event(
    title: str = Form(...),
    description: str = Form(...),
    date: date = Form(...),
    location: str = Form(...),
    flyer: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    flyer_path = None

    if flyer:
        flyer_path = f"{UPLOAD_DIR}/{flyer.filename}"
        with open(flyer_path, "wb") as f:
            f.write(flyer.file.read())

    event = Event(
        title=title,
        description=description,
        date=date,
        location=location,
        flyer=flyer_path,
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return {"message": "Event created", "event_id": event.id}



@router.get("/events/")
def list_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return events




