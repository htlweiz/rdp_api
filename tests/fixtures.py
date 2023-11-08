import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from rdp.crud.crud import Crud

@pytest.fixture(scope="function")
def crud_in_memory():
    engine = create_engine("sqlite:///:memory:")
    crud = Crud(engine)
    yield crud

@pytest.fixture(scope="function")
def crud_session_in_memory():
    engine = create_engine("sqlite:///:memory:")
    crud = Crud(engine)
    session = sessionmaker(bind=engine)
    yield (crud, session)
