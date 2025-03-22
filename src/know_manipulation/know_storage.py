from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

# --------------------------
#  Base de Conhecimento (SQLite)
# --------------------------

Base = declarative_base()

def generateSession():
    engine = create_engine('sqlite:///knowledge.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()