from sqlalchemy.orm import Session

from schemas import schemas
from repositories import supportOptionRepository, userRepository
from exceptions.exception import NotFoundException

def createOrUpdateSupportOption(db: Session, supportOption: schemas.CreateSupportOption, userId: int):
    dbSupporter = userRepository.getUser(db, userId=userId)
    if not dbSupporter:
        raise NotFoundException(message="supporter with such id not fount")
    dbBeneficiary = userRepository.getUser(db, userId=supportOption.beneficiaryId)
    if not dbBeneficiary:
        raise NotFoundException(message="beneficiary with such id not fount")
    return supportOptionRepository.createOrUpdateSupportOption(db, supportOption=supportOption, userId=userId)

def deleteSupportOption(db: Session, beneficiaryId: int, userId: int):
    dbSupporter = userRepository.getUser(db, userId=userId)
    if not dbSupporter:
        raise NotFoundException(message="supporter with such id not fount")
    dbBeneficiary = userRepository.getUser(db, userId=beneficiaryId)
    if not dbBeneficiary:
        raise NotFoundException(message="beneficiary with such id not fount")
    return supportOptionRepository.deleteSupportOption(db, beneficiaryId=beneficiaryId, userId=userId)

def getMySupporters(db: Session, userId: int, limit: int, skip: int):
    return supportOptionRepository.getMySupporters(db, userId=userId, limit=limit, skip=skip)

def getMyBeneficiaries(db: Session, userId: int, limit: int, skip: int):
    return supportOptionRepository.getMyBeneficiaries(db, userId=userId, limit=limit, skip=skip)
    