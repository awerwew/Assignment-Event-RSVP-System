import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, Form
from sqlalchemy.orm import Session
from datetime import date
from app.schemas.event_schema import EventCreate
from app.schemas.rsvp_schema import RSVPCreate

from app.core.security import decode_access_token
from app.models.user import User
from app.db.session import SessionLocal




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session =  Depends(get_db)
):
    data = decode_access_token(token)
    if data is None:
        raise HTTPException(status_code=401,detail="invalid authentication credentials")
    user = db.query(User).filter(User.email == data.get("sub")).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def get_current_active_user(
        current_user: User = Depends(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail= "inactive user")
    return current_user

def event_form(
    title: str = Form(...),
    description: str = Form(...),
    date: date = Form(...),
    location: str = Form(...),
) -> EventCreate:
    return EventCreate(
        title=title,
        description=description,
        date=date,
        location=location,
    )


UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


def rsvp_form(
    name: str = Form(...),
    email: str = Form(...),
       
) -> RSVPCreate:
    return RSVPCreate(
        name=name,
        email=email,
        
        
    )

