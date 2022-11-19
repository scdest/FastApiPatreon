from sqlalchemy.orm import Session

from schemas import schemas
from db import models

def createSupportOption(db: Session, supportOption: schemas.CreateSupportOption, userId: int):
    dbSupportOption = models.SupportOption(valueInUSD=supportOption.valueInUSD, supporterId=userId, beneficiaryId=supportOption.beneficiaryId)
    db.add(dbSupportOption)
    db.commit()
    db.refresh(dbSupportOption)
    return dbSupportOption

def getSupportOption(db: Session, beneficiaryId: int, supporterId: int):
    return db.query(models.SupportOption).filter(models.SupportOption.supporterId == supporterId).filter(models.SupportOption.beneficiaryId == beneficiaryId).first()

def updateSupportOption(db: Session, dbSupportOption: models.SupportOption):
    db.merge(dbSupportOption)
    db.commit()
    db.refresh(dbSupportOption)
    return dbSupportOption

def deleteSupportOption(db: Session, dbSupportOption: models.SupportOption):
    db.delete(dbSupportOption)
    db.commit()
    return True

def getMySupporters(db: Session, userId: int, skip: int = 0, limit: int = 100):
    return db.query(models.SupportOption).join(models.User, models.SupportOption.supporterId == models.User.id).filter(models.SupportOption.beneficiaryId == userId).offset(skip).limit(limit).all()

def getMyBeneficiaries(db: Session, userId: int, skip: int = 0, limit: int = 100):
    return db.query(models.SupportOption).join(models.User, models.SupportOption.beneficiaryId == models.User.id).filter(models.SupportOption.supporterId == userId).offset(skip).limit(limit).all()