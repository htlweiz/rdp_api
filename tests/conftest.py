import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from rdp.crud.crud import Crud
from rdp.crud.model import Base


@pytest.fixture(scope="function")
def crud_with_session():
    engine = create_engine("sqlite:///:memory:")

    Session = sessionmaker(bind=engine)

    yield (Crud(engine), Session)

    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def crud():
    engine = create_engine("sqlite:///:memory:")

    yield Crud(engine)

    Base.metadata.drop_all(engine)
