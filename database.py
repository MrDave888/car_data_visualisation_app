from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
import models  # registers all models with Base so create_all knows about every table

engine = create_engine('sqlite:///cars.db', echo=False)
Session = sessionmaker(bind=engine)


def init_db():
    """Create all tables in the database. Safe to call multiple times."""
    Base.metadata.create_all(engine)


def is_seeded():
    """Returns True if the database already has data."""
    from models import CarModel
    session = Session()
    try:
        return session.query(CarModel).count() > 0
    finally:
        session.close()
