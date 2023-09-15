import pytest
from sqlalchemy import create_engine

def test_create_engine():
    engine = create_engine("sqlite:///:memory:")  # Use an in-memory SQLite database for testing
    assert engine is not None
