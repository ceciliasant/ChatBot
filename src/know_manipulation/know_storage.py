from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

# --------------------------
#  Base de Conhecimento (SQLite)
# --------------------------
Base = declarative_base()
engine = create_engine('sqlite:///knowledge.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()