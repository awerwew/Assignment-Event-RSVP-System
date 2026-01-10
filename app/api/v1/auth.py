from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.user_schema import UserCreate, UserRead
from app.services.user_services import UserService
from app.schemas.auth_schema import LoginRequest, Token
from app.core.security import verify_password, create_access_token


router = APIRouter()

@router.post("/signup",response_model= UserRead, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    # checking existing user
    existing_user = UserService.get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="email already registered")
    #if user does not exist create a new user
    try:
        user = UserService.create_user(db, user_in)
        db.commit()
        return user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Internal server error"
        ) from e
    
    
@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = UserService.get_user_by_email(db, login_data.email)
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=400, detail="Invalid email or password"
        )
    access_token = create_access_token(email = user.email)
    return {"access_token": access_token, "token_type": "bearer"}
    
