from sqlalchemy import Column, ForeignKey, Integer, String, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)

class SupportOption(Base):
    __tablename__ = "support_options"

    valueInUSD = Column(Integer)
    supporterId = Column(Integer, ForeignKey("users.id"), primary_key=True)
    beneficiaryId = Column(Integer, ForeignKey("users.id"), primary_key=True)
    supporter = relationship("User", foreign_keys=[supporterId])
    beneficiary = relationship("User", foreign_keys=[beneficiaryId])

    PrimaryKeyConstraint("supporterId", "beneficiaryId")