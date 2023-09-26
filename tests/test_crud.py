from api.rdp.crud.model import ValueType


def test_001_dummy(): # dummy test, can't fail
    assert True



def test_002_valueType():
    # Create an instance of ValueType for testing
    value_type_instance = ValueType(id=1, type_name="tempType")
    
    assert repr(value_type_instance) == "ValueType(id=1, value_type='tempType')"