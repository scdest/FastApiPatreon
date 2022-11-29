from contextlib import AbstractContextManager
from typing import Callable, Iterator

from sqlalchemy.orm import Session

from .models import User, SupportOption
from .schemas import CreateUser, CreateSupportOption


class UserRepository:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_user(self, user_id: int) -> User:
        with self.session_factory() as session:
            return session.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> User:
        with self.session_factory() as session:
            return session.query(User).filter(User.email == email).first()
    
    def create_user(self, user: CreateUser) -> User:
        with self.session_factory() as session:
            db_user = User(email=user.email, name=user.name)
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return db_user

class SupportOptionRepository:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_support_option(self, beneficiary_id: int, supporter_id: int) -> SupportOption:
        with self.session_factory() as session:
            return session.query(SupportOption).filter(SupportOption.supporter_id == beneficiary_id).filter(SupportOption.beneficiary_id == supporter_id).first()
    
    def create_support_option(self, support_option: CreateSupportOption, user_id: int) -> SupportOption:
        with self.session_factory() as session:
            db_support_option = SupportOption(valueInUSD=support_option.value_in_USD, supporter_id=user_id, beneficiary_id=support_option.beneficiary_id)
            session.add(db_support_option)
            session.commit()
            session.refresh(db_support_option)
            return db_support_option
    
    def update_support_option(self, db_support_option: SupportOption) -> SupportOption:
        with self.session_factory() as session:
            session.merge(db_support_option)
            session.commit()
            session.refresh(db_support_option)
            return db_support_option

    def delete_support_option(self, db_support_option: SupportOption) -> bool:
        with self.session_factory() as session:
            session.delete(db_support_option)
            session.commit()
            return True

    def get_my_supporters(self, user_id: int,  skip: int = 0, limit: int = 100) -> Iterator[SupportOption]:
        with self.session_factory() as session:
            return session.query(SupportOption).join(User, SupportOption.supporter_id == User.id).filter(SupportOption.beneficiary_id == user_id).offset(skip).limit(limit).all()
    
    def get_my_beneficiaries(self, user_id: int,  skip: int = 0, limit: int = 100) -> Iterator[SupportOption]:
        with self.session_factory() as session:
            return session.query(SupportOption).join(User, SupportOption.beneficiary_id == User.id).filter(SupportOption.supporter_id == user_id).offset(skip).limit(limit).all()