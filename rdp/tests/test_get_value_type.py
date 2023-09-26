from typing import Tuple, Type

import pytest
from rdp.crud.crud import Crud
from sqlalchemy.orm import Session

CrudSession = Type[Tuple[Crud, Type[Session]]]


def test_add_or_update_value_type(crud_with_session: CrudSession):
    crud, Session = crud_with_session
    value_type_id = 1
    value_type_name = "TestType"
    value_type_unit = "TestUnit"

    new_value_type = crud.add_or_update_value_type(value_type_id, value_type_name, value_type_unit)
    assert new_value_type.id == value_type_id
    assert new_value_type.type_name == value_type_name
    assert new_value_type.type_unit == value_type_unit
