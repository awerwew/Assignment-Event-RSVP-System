from fastapi import FastAPI
from app.api.v1 import event_route
from app.api.v1 import rsvp_route
from app.api.v1 import auth
from app.core.config import settings


app = FastAPI(title="FastAPI Event systems app")

app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])
app.include_router(event_route.router, prefix=settings.API_V1_STR, tags=["Event"])
app.include_router(rsvp_route.router, prefix=settings.API_V1_STR, tags=["RSVP"])




@app.get("/", tags=["Home"])
def read_root():
    return {"message": "Welcome to Event System App"}
    
