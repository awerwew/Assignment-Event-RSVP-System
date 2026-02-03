
from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.rsvp import RSVP
from app.api.deps import get_current_active_user, rsvp_form
from app.models.user import User
from app.schemas.rsvp_schema import RSVPCreate

router = APIRouter()



@router.post("/events/{event_id}/rsvp", status_code=201)
def rsvp_event(
    event_id: int,
    rsvp_data: RSVPCreate = Depends(rsvp_form),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
     # prevent duplicate RSVP
    existing = (
        db.query(RSVP)
        .filter(RSVP.event_id == event_id, RSVP.email == rsvp_data.email)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="You already RSVP’d")

    rsvp = RSVP(
        name=rsvp_data.name,
        email=rsvp_data.email,
        event_id=event_id,
    )

    db.add(rsvp)
    db.commit()
    db.refresh(rsvp)

    return {"message": "RSVP successful"}

@router.get("/events/{event_id}/rsvps")
def get_rsvps(
    event_id: int, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    ):
    rsvps = db.query(RSVP).filter(RSVP.event_id == event_id).all()
    if not rsvps:
        raise HTTPException(status_code=404, detail="Event with id not found")
    return rsvps
