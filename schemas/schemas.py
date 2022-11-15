from pydantic import BaseModel, PositiveInt
class UserBase(BaseModel):
    email: str
    name: str
class CreateUser(UserBase):
    pass
class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class CreateSupportOption(BaseModel):
    valueInUSD: PositiveInt
    beneficiaryId: int
class SupportOption(CreateSupportOption):
    supporterId: int

    class Config:
        orm_mode = True

class Supporter(SupportOption):
    supporter: User

class Beneficiary(SupportOption):
    beneficiary: User
