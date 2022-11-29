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

    value_in_USD = Column(Integer)
    supporter_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    beneficiary_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    supporter = relationship("User", foreign_keys=[supporter_id])
    beneficiary = relationship("User", foreign_keys=[beneficiary_id])

    PrimaryKeyConstraint("supporter_id", "beneficiary_id")