from sqlalchemy.orm import Session

from schemas import schemas
from db import models

def createOrUpdateSupportOption(db: Session, supportOption: schemas.CreateSupportOption, userId: int):
    dbSupportOption = db.query(models.SupportOption).filter(models.SupportOption.supporterId == userId).filter(models.SupportOption.beneficiaryId == supportOption.beneficiaryId).first()
    if dbSupportOption:
        dbSupportOption.valueInUSD = supportOption.valueInUSD
        db.merge(dbSupportOption)
    else:
        dbSupportOption = models.SupportOption(valueInUSD=supportOption.valueInUSD, supporterId=userId, beneficiaryId=supportOption.beneficiaryId)
        db.add(dbSupportOption)
    db.commit()
    db.refresh(dbSupportOption)
    return dbSupportOption

def deleteSupportOption(db: Session, beneficiaryId: int, userId: int):
    dbSupportOption = db.query(models.SupportOption).filter(models.SupportOption.beneficiaryId == beneficiaryId).filter(models.SupportOption.supporterId == userId).first()
    if dbSupportOption:
        db.delete(dbSupportOption)
        db.commit()
        return True
    return False

def getMySupporters(db: Session, userId: int, skip: int = 0, limit: int = 100):
    return db.query(models.SupportOption).join(models.User, models.SupportOption.supporterId == models.User.id).filter(models.SupportOption.beneficiaryId == userId).offset(skip).limit(limit).all()

def getMyBeneficiaries(db: Session, userId: int, skip: int = 0, limit: int = 100):
    return db.query(models.SupportOption).join(models.User, models.SupportOption.beneficiaryId == models.User.id).filter(models.SupportOption.supporterId == userId).offset(skip).limit(limit).all()