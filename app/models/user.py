from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from datetime import datetime, timezone

from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index = True)
    email = Column(String, unique = True, index = True, nullable = False)
    hashed_password = Column(String, nullable = False)
    is_active = Column(Boolean, default=True)
    full_name = Column(String, index = True)
    is_superuser = Column(Boolean, default = False)
    created_at = Column(DateTime(timezone = True), default = datetime.now(timezone.utc))