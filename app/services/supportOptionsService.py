from sqlalchemy.orm import Session

from app.schemas import schemas
from app.repositories import supportOptionRepository, userRepository
from app.exceptions.exception import NotFoundException

def createOrUpdateSupportOption(db: Session, supportOption: schemas.CreateSupportOption, userId: int):
    dbSupporter = userRepository.getUser(db, userId=userId)
    if not dbSupporter:
        raise NotFoundException(message="supporter with such id not fount")
    dbBeneficiary = userRepository.getUser(db, userId=supportOption.beneficiaryId)
    if not dbBeneficiary:
        raise NotFoundException(message="beneficiary with such id not fount")
    
    dbSupportOption = supportOptionRepository.getSupportOption(db, beneficiaryId=supportOption.beneficiaryId, supporterId=userId)

    if dbSupportOption:
        dbSupportOption.valueInUSD = supportOption.valueInUSD
        return supportOptionRepository.updateSupportOption(db, dbSupportOption=dbSupportOption)
    else: 
        return supportOptionRepository.createSupportOption(db, supportOption=supportOption, userId=userId)


def deleteSupportOption(db: Session, beneficiaryId: int, userId: int):
    dbSupporter = userRepository.getUser(db, userId=userId)
    if not dbSupporter:
        raise NotFoundException(message="supporter with such id not fount")
    dbBeneficiary = userRepository.getUser(db, userId=beneficiaryId)
    if not dbBeneficiary:
        raise NotFoundException(message="beneficiary with such id not fount")

    dbSupportOption = supportOptionRepository.getSupportOption(db, beneficiaryId=beneficiaryId, supporterId=userId)
    if dbSupportOption:
        return supportOptionRepository.deleteSupportOption(db, dbSupportOption=dbSupportOption)
    else:
        return False

def getMySupporters(db: Session, userId: int, limit: int, skip: int):
    return supportOptionRepository.getMySupporters(db, userId=userId, limit=limit, skip=skip)

def getMyBeneficiaries(db: Session, userId: int, limit: int, skip: int):
    return supportOptionRepository.getMyBeneficiaries(db, userId=userId, limit=limit, skip=skip)
    