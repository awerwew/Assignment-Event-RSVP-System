from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import os
import shutil
from app.api.deps import get_db, event_form, UPLOAD_DIR
from app.models.event import Event


from app.schemas.event_schema import  EventCreate

#this is trial
from app.models.user import User
from app.api.deps import get_current_active_user


router = APIRouter()





@router.post("/events/", status_code=201)
def create_event(
    event_data: EventCreate = Depends(event_form),
    flyer: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    flyer_path = None

    if flyer:
        flyer_path = os.path.join(UPLOAD_DIR, flyer.filename)
        with open(flyer_path, "wb") as f:
            shutil.copyfileobj(flyer.file, f)

    event = Event(
        title=event_data.title,
        description=event_data.description,
        date=event_data.date,
        location=event_data.location,
        flyer=flyer_path,
       
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    
    
    return {"message": "Event created", "event_id": event.id}



@router.get("/events/")
def list_events(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    ):
    events = db.query(Event).all()
    return events


@router.get("/events/{event_id}")
def get_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return event



