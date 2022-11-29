from uuid import uuid4
from typing import Iterator

from .repositories import UserRepository, SupportOptionRepository
from .models import User, SupportOption
from .schemas import CreateUser, CreateSupportOption
from .exception import AlreadyExistsException, NotFoundException


class UserService:

    def __init__(self, user_repository: UserRepository) -> None:
        self._repository: UserRepository = user_repository

    def get_user(self, user_id: int) -> User:
        db_user = self._repository.get_user(user_id=user_id)
        if not db_user:
            raise NotFoundException(message="user with such id not found")
        return db_user

    def create_user(self, user: CreateUser) -> User:
        db_user = self._repository.get_user_by_email(email=user.email)
        if db_user:
            raise AlreadyExistsException(message="user with such email already registered")
        return self._repository.create_user(user=user)

class SupportOptionService:

    def __init__(self, user_repository: UserRepository, support_option_repository: SupportOptionRepository) -> None:
        self._user_repository: UserRepository = user_repository
        self._support_option_repository: SupportOptionRepository = support_option_repository

    def create_or_update_support_option(self, support_option: CreateSupportOption, user_id: int) -> SupportOption:
        db_supporter = self._user_repository.get_user(user_id=user_id)
        if not db_supporter:
            raise NotFoundException(message="supporter with such id not fount")
        db_beneficiary = self._user_repository.get_user(user_id=support_option.beneficiary_id)
        if not db_beneficiary:
            raise NotFoundException(message="beneficiary with such id not fount")
    
        db_support_option = self._support_option_repository.get_support_option(beneficiary_id=support_option.beneficiary_id, supporter_id=user_id)

        if db_support_option:
            db_support_option.value_in_USD = support_option.value_in_USD
            return self._support_option_repository.update_support_option(db_support_option=db_support_option)
        else: 
            return self._support_option_repository.create_support_option(support_option=support_option, user_id=user_id)


    def delete_support_option(self, beneficiary_id: int, user_id: int) -> bool:
        db_supporter = self._user_repository.get_user(user_id=user_id)
        if not db_supporter:
            raise NotFoundException(message="supporter with such id not fount")
        db_beneficiary = self._user_repository.get_user(user_id=beneficiary_id)
        if not db_beneficiary:
            raise NotFoundException(message="beneficiary with such id not fount")

        db_support_option = self._support_option_repository.get_support_option(beneficiary_id=beneficiary_id, supporter_id=user_id)

        if db_support_option:
            return self._support_option_repository.delete_support_option(db_support_option=db_support_option)
        else: 
            return False

    def get_my_supporters(self, user_id: int, limit: int, skip: int):
        return self._support_option_repository.get_my_supporters(user_id=user_id, limit=limit, skip=skip)

    def get_my_beneficiaries(self, user_id: int, limit: int, skip: int):
        return self._support_option_repository.get_my_beneficiaries(user_id=user_id, limit=limit, skip=skip)