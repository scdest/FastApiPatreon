from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

load_dotenv()

from app.db import models
from app.schemas import schemas
from app.services import userService, supportOptionsService
from app.db.database import SessionLocal, engine
from app.exceptions.exception import AlreadyExistsException, NotFoundException


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.exception_handler(AlreadyExistsException)
def alreadyExistsExceptionHandler(request: Request, exc: AlreadyExistsException):
    return JSONResponse(
        status_code=400,
        content={'message': exc.message}
    )

@app.exception_handler(NotFoundException)
def notFoundExceptionHandler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content={'message': exc.message}
    )


@app.post("/users/", response_model=schemas.User)
def createUser(user: schemas.UserBase, db: Session = Depends(get_db)):
    return userService.createUser(db=db, user=user)

@app.get("/users/{userId}", response_model=schemas.User)
def readUser(userId: int, db: Session = Depends(get_db)):
    return userService.getUser(db, userId=userId)

@app.post("/support-options/", response_model=schemas.SupportOption)
def createOrUpdateSupportOption(supportOption: schemas.CreateSupportOption, AUTH_USER_ID: int | None = Header(default=None), db: Session = Depends(get_db)):
    return supportOptionsService.createOrUpdateSupportOption(db=db, userId=AUTH_USER_ID, supportOption=supportOption)

@app.delete("/support-options/beneficiaries/{beneficiaryId}", response_model=bool)
def createOrUpdateSupportOption(beneficiaryId: int, AUTH_USER_ID: int | None = Header(default=None), db: Session = Depends(get_db)):
    return supportOptionsService.deleteSupportOption(db, beneficiaryId=beneficiaryId, userId=AUTH_USER_ID)

@app.get("/my-supporters/", response_model=list[schemas.Supporter])
def createSupportOption(skip: int = 0, limit: int = 100, AUTH_USER_ID: int | None = Header(default=None), db: Session = Depends(get_db)):
    return supportOptionsService.getMySupporters(db, userId=AUTH_USER_ID, skip=skip, limit=limit)

@app.get("/my-beneficiaries/", response_model=list[schemas.Beneficiary])
def createSupportOption(skip: int = 0, limit: int = 100, AUTH_USER_ID: int | None = Header(default=None), db: Session = Depends(get_db)):
    return supportOptionsService.getMySupporters(db, userId=AUTH_USER_ID, skip=skip, limit=limit)

