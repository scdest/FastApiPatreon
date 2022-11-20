from sqlalchemy.orm import Session

from app.schemas import schemas
from app.repositories import userRepository
from app.exceptions.exception import AlreadyExistsException, NotFoundException

def createUser(db: Session, user: schemas.UserBase):
    db_user = userRepository.getUserByEmail(db, email=user.email)
    if db_user:
        raise AlreadyExistsException(message="user with such email already registered")
    return userRepository.createUser(db, user)

def getUser(db: Session, userId: int):
    dbUser = userRepository.getUser(db, userId=userId)
    if not dbUser:
        raise NotFoundException(message="user with such id not found")
    return dbUser

    