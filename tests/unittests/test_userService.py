from unittest.mock import patch, Mock, MagicMock
import pytest
from sqlalchemy.orm import Session
from app.exceptions.exception import AlreadyExistsException, NotFoundException
from app.schemas.schemas import UserBase
from app.services import userService

@patch('app.repositories.userRepository.getUserByEmail')
@patch('app.repositories.userRepository.createUser')
def test_create_user(createUser: MagicMock, getUserByEmail: MagicMock):
    db = Mock(Session)
    user = UserBase(email="test@test", name="John")
    getUserByEmail.return_value = None

    userService.createUser(db, user)

    getUserByEmail.assert_called_once_with(db, email=user.email)
    createUser.assert_called_once_with(db, user)

@patch('app.repositories.userRepository.getUserByEmail')
@patch('app.repositories.userRepository.createUser')
def test_user_exists(createUser: MagicMock, getUserByEmail: MagicMock):
    with pytest.raises(AlreadyExistsException) as exc_info:

        db = Mock(Session)
        user = UserBase(email="test@test", name="John")

        userService.createUser(db, user)
    
    assert exc_info.value.message == "user with such email already registered"
    getUserByEmail.assert_called_once_with(db, email=user.email)
    createUser.assert_not_called()

@patch('app.repositories.userRepository.getUser')
def test_get_user(getUser: MagicMock):
    db = Mock(Session)
    userId = 23

    userService.getUser(db, userId)

    getUser.assert_called_once_with(db, userId=userId)

@patch('app.repositories.userRepository.getUser')
def test_get_user_does_not_exist(getUser: MagicMock):
    with pytest.raises(NotFoundException) as exc_info:

        db = Mock(Session)
        userId = 23
        getUser.return_value = None

        userService.getUser(db, userId=userId)
    
    assert exc_info.value.message == "user with such id not found"
    getUser.assert_called_once_with(db, userId=userId)