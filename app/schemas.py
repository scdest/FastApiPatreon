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
    value_in_USD: PositiveInt
    beneficiary_id: int
class SupportOption(CreateSupportOption):
    supporter_id: int

    class Config:
        orm_mode = True

class Supporter(SupportOption):
    supporter: User

class Beneficiary(SupportOption):
    beneficiary: User
