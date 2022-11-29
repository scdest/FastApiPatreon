from unittest.mock import Mock, call
import pytest
from app.exception import NotFoundException
from app.schemas import CreateSupportOption
from app.models import User, SupportOption
from app.repositories import UserRepository, SupportOptionRepository
from app.services import SupportOptionService

def test_create_or_update_support_option_supporter_not_found():
    with pytest.raises(NotFoundException) as exc_info:
        user_repository = Mock(UserRepository)
        support_option_repository = Mock(SupportOptionRepository)
        support_option_service = SupportOptionService(user_repository=user_repository, support_option_repository=support_option_repository)
        support_option = CreateSupportOption(value_in_USD=10, beneficiary_id=1)
        user_id = 2
        user_repository.get_user.return_value = None

        support_option_service.create_or_update_support_option(support_option=support_option, user_id=user_id)
    assert exc_info.value.message == "supporter with such id not fount"
    user_repository.get_user.assert_called_once_with(user_id=user_id)

def test_create_or_update_support_option_beneficiary_not_found():
    with pytest.raises(NotFoundException) as exc_info:
        user_repository = Mock(UserRepository)
        support_option_repository = Mock(SupportOptionRepository)
        support_option_service = SupportOptionService(user_repository=user_repository, support_option_repository=support_option_repository)
        supporter = Mock(User)
        support_option = CreateSupportOption(value_in_USD=10, beneficiary_id=1)
        user_id = 2
        user_repository.get_user.side_effect = [supporter, None]

        support_option_service.create_or_update_support_option(support_option=support_option, user_id=user_id)
    assert exc_info.value.message == "beneficiary with such id not fount"
    user_repository.get_user.assert_has_calls([
        call(user_id=user_id),
        call(user_id=support_option.beneficiary_id)
    ])

def test_create_or_update_support_option_create():
    user_repository = Mock(UserRepository)
    support_option_repository = Mock(SupportOptionRepository)
    support_option_service = SupportOptionService(user_repository=user_repository, support_option_repository=support_option_repository)

    support_option = CreateSupportOption(value_in_USD=10, beneficiary_id=1)
    user_id = 2

    support_option_repository.get_support_option.return_value = None

    support_option_service.create_or_update_support_option(support_option=support_option, user_id=user_id)
    support_option_repository.create_support_option.assert_called_once_with(support_option=support_option, user_id=user_id)
    support_option_repository.update_support_option.assert_not_called()

def test_create_or_update_support_option_update():
    user_repository = Mock(UserRepository)
    support_option_repository = Mock(SupportOptionRepository)
    support_option_service = SupportOptionService(user_repository=user_repository, support_option_repository=support_option_repository)

    support_option = CreateSupportOption(value_in_USD=10, beneficiary_id=1)
    user_id = 2

    db_support_option = Mock(SupportOption)
    db_support_option.value_in_USD = 5

    support_option_repository.get_support_option.return_value = db_support_option

    support_option_service.create_or_update_support_option(support_option=support_option, user_id=user_id)

    assert db_support_option.value_in_USD == 10
    support_option_repository.get_support_option.assert_called_once_with(beneficiary_id=support_option.beneficiary_id, supporter_id=user_id)
    support_option_repository.update_support_option.assert_called_once_with(db_support_option=db_support_option)
    support_option_repository.create_support_option.assert_not_called()

def test_delete_support_option():
    user_repository = Mock(UserRepository)
    support_option_repository = Mock(SupportOptionRepository)
    support_option_service = SupportOptionService(user_repository=user_repository, support_option_repository=support_option_repository)

    user_id = 2
    beneficiary_id = 1
    db_support_option = Mock(SupportOption)

    support_option_repository.get_support_option.return_value = db_support_option

    res = support_option_service.delete_support_option(beneficiary_id=beneficiary_id, user_id=user_id)

    support_option_repository.delete_support_option.assert_called_once_with(db_support_option=db_support_option)
    assert res

def test_delete_not_exist():
    user_repository = Mock(UserRepository)
    support_option_repository = Mock(SupportOptionRepository)
    support_option_service = SupportOptionService(user_repository=user_repository, support_option_repository=support_option_repository)

    user_id = 2
    beneficiary_id = 1

    support_option_repository.get_support_option.return_value = None

    res = support_option_service.delete_support_option(beneficiary_id=beneficiary_id, user_id=user_id)
    support_option_repository.delete_support_option.assert_not_called()
    assert res == False

def test_get_my_supporters():
    user_repository = Mock(UserRepository)
    support_option_repository = Mock(SupportOptionRepository)
    support_option_service = SupportOptionService(user_repository=user_repository, support_option_repository=support_option_repository)

    user_id = 2
    limit = 50
    skip = 10

    support_option_service.get_my_supporters(user_id=user_id, limit=limit, skip=skip)

    support_option_repository.get_my_supporters.assert_called_once_with(user_id=user_id, limit=limit, skip=skip)

def test_get_my_beneficiaries():
    user_repository = Mock(UserRepository)
    support_option_repository = Mock(SupportOptionRepository)
    support_option_service = SupportOptionService(user_repository=user_repository, support_option_repository=support_option_repository)

    user_id = 2
    limit = 50
    skip = 10

    support_option_service.get_my_beneficiaries(user_id=user_id, limit=limit, skip=skip)

    support_option_repository.get_my_beneficiaries.assert_called_once_with(user_id=user_id, limit=limit, skip=skip)
