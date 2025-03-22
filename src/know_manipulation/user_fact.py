from sqlalchemy import Column, String, Integer

from know_manipulation.know_storage import Base

class UserFact(Base):
    __tablename__ = 'user_facts'
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    key = Column(String)  # Entidade (ex: "cat")
    value = Column(String)  # Fato (ex: "is on the floor")
