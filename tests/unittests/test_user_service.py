from unittest.mock import Mock
import pytest
from app.exception import AlreadyExistsException, NotFoundException
from app.schemas import CreateUser
from app.services import UserService
from app.repositories import UserRepository

def test_create_user():
    user_repository = Mock(UserRepository)
    user = CreateUser(email="test@test", name="John")
    user_repository.get_user_by_email.return_value = None

    user_service = UserService(user_repository=user_repository)

    user_service.create_user(user=user)

    user_repository.get_user_by_email.assert_called_once_with(email=user.email)
    user_repository.create_user.assert_called_once_with(user=user)

def test_user_exists():
    with pytest.raises(AlreadyExistsException) as exc_info:
        user = CreateUser(email="test@test", name="John")
        user_repository = Mock(UserRepository)
        user_service = UserService(user_repository=user_repository)
        user_service.create_user(user=user)
    
    assert exc_info.value.message == "user with such email already registered"
    user_repository.get_user_by_email.assert_called_once_with(email=user.email)
    user_repository.create_user.assert_not_called()

def test_get_user():
    user_id = 23
    user_repository = Mock(UserRepository)
    user_service = UserService(user_repository=user_repository)
    user_service.get_user(user_id=user_id)

    user_repository.get_user.assert_called_once_with(user_id=user_id)

def test_get_user_does_not_exist():
    with pytest.raises(NotFoundException) as exc_info:

        user_repository = Mock(UserRepository)
        user_service = UserService(user_repository=user_repository)
        user_id = 23
        user_repository.get_user.return_value = None

        user_service.get_user(user_id=user_id)
    
    assert exc_info.value.message == "user with such id not found"
    user_repository.get_user.assert_called_once_with(user_id=user_id)