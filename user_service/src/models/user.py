from sqlalchemy import Column, Integer, String

from user_service.src.db import Base

class User(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
