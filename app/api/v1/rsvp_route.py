
from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.rsvp import RSVP

router = APIRouter()



@router.post("/events/{event_id}/rsvp", status_code=201)
def rsvp_event(
    event_id: int,
    name: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db),
):
     # prevent duplicate RSVP
    existing = (
        db.query(RSVP)
        .filter(RSVP.event_id == event_id, RSVP.email == email)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="You already RSVP’d")

    rsvp = RSVP(
        name=name,
        email=email,
        event_id=event_id,
    )

    db.add(rsvp)
    db.commit()
    db.refresh(rsvp)

    return {"message": "RSVP successful"}

@router.get("/events/{event_id}/rsvps")
def get_rsvps(event_id: int, db: Session = Depends(get_db)):
    rsvps = db.query(RSVP).filter(RSVP.event_id == event_id).all()
    if not rsvps:
        raise HTTPException(status_code=404, detail="Event with id not found")
    return rsvps
