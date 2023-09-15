import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from rdp.crud.crud import Crud  # Adjust the import path as needed
from rdp.crud.model import Base

DB_URL = "sqlite:///:memory:"
engine = create_engine(DB_URL)

Base.metadata.create_all(engine)

@pytest.fixture(scope="function")
def database_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    session.begin()
    yield session
    session.rollback()
    session.close()
