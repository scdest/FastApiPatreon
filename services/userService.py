from sqlalchemy.orm import Session

from schemas import schemas
from repositories import userRepository
from exceptions.exception import AlreadyExistsException, NotFoundException

def createUser(db: Session, user: schemas.UserBase):
    db_user = userRepository.getUserByEmail(db, email=user.email)
    if db_user:
        raise AlreadyExistsException(message="user with such email already registered")
    return userRepository.createUser(db, user)

def getUser(db: Session, userId: int):
    dbUser = userRepository.getUser(db, userId=userId)
    if not dbUser:
        raise NotFoundException(message="user with such id not fount")
    return dbUser

    