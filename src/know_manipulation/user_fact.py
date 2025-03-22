from sqlalchemy import Column, String, Integer, Enum

from know_manipulation.know_storage import Base
from know_manipulation.fact_types import RELATION_KEYS

class UserFact(Base):
    __tablename__ = 'user_facts'
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    key = Column(String)  # Entidade (ex: "cat")
    value = Column(String)  # Fato (ex: "on the floor")
    fact_type = Column(Enum(*RELATION_KEYS, name="relation_type_enum"))  # Fato (ex: "is", "is a")
