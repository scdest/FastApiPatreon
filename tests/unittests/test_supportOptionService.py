from unittest.mock import patch, Mock, MagicMock, call
import pytest
from sqlalchemy.orm import Session
from db.models import User, SupportOption
from exceptions.exception import NotFoundException
from schemas.schemas import CreateSupportOption
from services import supportOptionsService

@patch('repositories.userRepository.getUser')
def test_createOrUpdateSupportOption_supporter_not_found(getUser: MagicMock):
    with pytest.raises(NotFoundException) as exc_info:
        db = Mock(Session)
        supportOption = CreateSupportOption(valueInUSD=10, beneficiaryId=1)
        userId = 2
        getUser.return_value = None

        supportOptionsService.createOrUpdateSupportOption(db, supportOption=supportOption, userId=userId)
    assert exc_info.value.message == "supporter with such id not fount"
    getUser.assert_called_once_with(db, userId=userId)

@patch('repositories.userRepository.getUser')
def test_createOrUpdateSupportOption_beneficiary_not_found(getUser: MagicMock):
    with pytest.raises(NotFoundException) as exc_info:
        db = Mock(Session)
        supporter = Mock(User)
        supportOption = CreateSupportOption(valueInUSD=10, beneficiaryId=1)
        userId = 2
        getUser.side_effect = [supporter, None]

        supportOptionsService.createOrUpdateSupportOption(db, supportOption=supportOption, userId=userId)
    assert exc_info.value.message == "beneficiary with such id not fount"
    getUser.assert_has_calls([
        call(db, userId=userId),
        call(db, userId=supportOption.beneficiaryId)
    ])

@patch('repositories.supportOptionRepository.getSupportOption')
@patch('repositories.supportOptionRepository.createSupportOption')
@patch('repositories.supportOptionRepository.updateSupportOption')
def test_createOrUpdateSupportOption_create(updateSupportOption: MagicMock, createSupportOption: MagicMock, getSupportOption: MagicMock):
    db = Mock(Session)

    supportOption = CreateSupportOption(valueInUSD=10, beneficiaryId=1)
    userId = 2

    getSupportOption.return_value = None

    supportOptionsService.createOrUpdateSupportOption(db, supportOption=supportOption, userId=userId)
    createSupportOption.assert_called_once_with(db, supportOption=supportOption, userId=userId)
    updateSupportOption.assert_not_called()

@patch('repositories.supportOptionRepository.getSupportOption')
@patch('repositories.supportOptionRepository.createSupportOption')
@patch('repositories.supportOptionRepository.updateSupportOption')
def test_createOrUpdateSupportOption_update(updateSupportOption: MagicMock, createSupportOption: MagicMock, getSupportOption: MagicMock):
    db = Mock(Session)

    supportOption = CreateSupportOption(valueInUSD=10, beneficiaryId=1)
    userId = 2
    dbSupportOption = Mock(SupportOption)
    dbSupportOption.valueInUSD = 5

    getSupportOption.return_value = dbSupportOption

    supportOptionsService.createOrUpdateSupportOption(db, supportOption=supportOption, userId=userId)

    assert dbSupportOption.valueInUSD == 10
    getSupportOption.assert_called_once_with(db, beneficiaryId=supportOption.beneficiaryId, supporterId=userId)
    updateSupportOption.assert_called_once_with(db, dbSupportOption=dbSupportOption)
    createSupportOption.assert_not_called()


@patch('repositories.supportOptionRepository.getSupportOption')
@patch('repositories.supportOptionRepository.deleteSupportOption')
def test_deleteOrUpdateSupportOption(deleteSupportOption: MagicMock, getSupportOption: MagicMock):
    db = Mock(Session)

    userId = 2
    beneficiaryId = 1
    dbSupportOption = Mock(SupportOption)

    getSupportOption.return_value = dbSupportOption

    res = supportOptionsService.deleteSupportOption(db, beneficiaryId=beneficiaryId, userId=userId)

    deleteSupportOption.assert_called_once_with(db, dbSupportOption=dbSupportOption)
    assert res

@patch('repositories.supportOptionRepository.getSupportOption')
@patch('repositories.supportOptionRepository.deleteSupportOption')
def test_deleteOrUpdateSupportOption_not_exist(deleteSupportOption: MagicMock, getSupportOption: MagicMock):
    db = Mock(Session)

    userId = 2
    beneficiaryId = 1

    getSupportOption.return_value = None

    res = supportOptionsService.deleteSupportOption(db, beneficiaryId=beneficiaryId, userId=userId)

    deleteSupportOption.assert_not_called()
    assert res == False

@patch('repositories.supportOptionRepository.getMySupporters')
def test_getMySupporters(getMySupporters: MagicMock):
    db = Mock(Session)

    userId = 2
    limit = 50
    skip = 10

    supportOptionsService.getMySupporters(db, userId=userId, limit=limit, skip=skip)

    getMySupporters.assert_called_once_with(db, userId=userId, limit=limit, skip=skip)

@patch('repositories.supportOptionRepository.getMyBeneficiaries')
def test_getMySupporters(getMyBeneficiaries: MagicMock):
    db = Mock(Session)

    userId = 2
    limit = 50
    skip = 10

    supportOptionsService.getMyBeneficiaries(db, userId=userId, limit=limit, skip=skip)

    getMyBeneficiaries.assert_called_once_with(db, userId=userId, limit=limit, skip=skip)
