from sqlalchemy.orm import Session

from schemas import schemas
from db import models


def getUser(db: Session, userId: int):
    return db.query(models.User).filter(models.User.id == userId).first()

def getUserByEmail(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def getUsers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def createUser(db: Session, user: schemas.UserBase):
    db_user = models.User(email=user.email, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
