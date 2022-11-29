from fastapi import APIRouter, Depends, Header
from dependency_injector.wiring import inject, Provide

from .containers import Container
from .services import UserService, SupportOptionService
from .schemas import CreateUser, CreateSupportOption, User, Supporter, SupportOption, Beneficiary

router = APIRouter()

@router.post("/users/", response_model=User)
@inject
def create_user(user: CreateUser, user_service: UserService = Depends(Provide[Container.user_service])):
    return user_service.create_user(user=user)

@router.get("/users/{user_id}", response_model=User)
@inject
def read_user(user_id: int, user_service: UserService = Depends(Provide[Container.user_service])):
    return user_service.get_user(user_id=user_id)

@router.post("/support-options/", response_model=SupportOption)
@inject
def create_or_update_support_option(
    support_option: CreateSupportOption, 
    AUTH_USER_ID: int | None = Header(default=None), 
    support_option_service: SupportOptionService = Depends(Provide[Container.support_option_service])
):
    return support_option_service.create_or_update_support_option(support_option=support_option, user_id=AUTH_USER_ID)

@router.delete("/support-options/beneficiaries/{beneficiary_id}", response_model=bool)
@inject
def delete_support_option(
    beneficiary_id: int, 
    AUTH_USER_ID: int | None = Header(default=None), 
    support_option_service: SupportOptionService = Depends(Provide[Container.support_option_service])
):
    return support_option_service.delete_support_option(beneficiary_id=beneficiary_id, user_id=AUTH_USER_ID)

@router.get("/my-supporters/", response_model=list[Supporter])
@inject
def get_my_supporters(
    skip: int = 0, 
    limit: int = 100, 
    AUTH_USER_ID: int | None = Header(default=None), 
    support_option_service: SupportOptionService = Depends(Provide[Container.support_option_service])
):
    return support_option_service.get_my_supporters(user_id=AUTH_USER_ID, limit=limit, skip=skip)

@router.get("/my-beneficiaries/", response_model=list[Beneficiary])
@inject
def get_my_beneficiaries(
    skip: int = 0, 
    limit: int = 100, 
    AUTH_USER_ID: int | None = Header(default=None), 
    support_option_service: SupportOptionService = Depends(Provide[Container.support_option_service])
):
    return support_option_service.get_my_beneficiaries(user_id=AUTH_USER_ID, skip=skip, limit=limit)