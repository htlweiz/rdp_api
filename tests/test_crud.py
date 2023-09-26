import sqlalchemy as db
from sqlalchemy import select, create_engine
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import registry, Session

from api.rdp.crud import Crud, create_engine
# from rdp.crud.crud import Crud #, model

class TestCases:

    def test_01_add_value_type(self):

        test_data_type = ["Rain", "Wind Speed"]
        test_data_type_id = [3, None ] # Temperature, Humidity, Pressure
        test_data_unit = ["ml", "K"]

        # first check if db is empty 
        # add values but with None and check count
        # add values but with real names and check count

        self.engine = db.create_engine("sqlite:///:memory:")
        crud = Crud(self.engine)

        for i, value in enumerate(test_data_type):
            result = crud.add_or_update_value_type()

        """
        with Session(self._engine) as session:

            session.add_all([db_type])
            session.commit()
        """

    def test_02_update_value_type(self):

        # first check if db is empty 
        # add values but with None and check count
        # add values but with real names and check count

        """
        with Session(self._engine) as session:

            session.add_all([db_type])
            session.commit()
        """

    def test_03_add_value(self):

        test_data_time = ["1695565645", "1695565646", "1695565647"]
        test_data_type = [0, 1, 2 ] # Temperature, Humidity, Pressure
        test_data_value = [17.2999992370605, 94.0, 978.0]
        
        self.engine = db.create_engine("sqlite:///:memory:")
        crud = Crud(self.engine)

        size_before = crud.get_values()

        for i, value in enumerate(test_data_time):
            crud.add_value(test_data_time[i],
                           test_data_type[i],
                           test_data_value[i])

        size_after = crud.get_values()
        assert size_before < size_after
        assert size_before != size_after

    def test_04_get_value_types(self):

        test_data_types = ["Temperature", "Humidity", "Pressure"]

        # self.engine = db.create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
        self.engine = create_engine("sqlite:///api/tests/test_db.db")
        crud = Crud(self.engine)
        test_result = crud.get_value_types()
        # what does the return look like ??

        assert len(test_result) == 3

        for i, value in enumerate(test_data_types):
            assert test_data_types[i] == test_result[i].type_name

    def test_05_get_value_type(self):

        test_data_type_id = [0, 1, 2 ]
        test_data_types = ["Temperature", "Humidity", "Pressure"]

        self.engine = db.create_engine("sqlite:///api/tests/test_db.db")
        crud = Crud(self.engine)

        for i in test_data_type_id:
            test_result = crud.get_value_type(i)
            # what does the return look like ??
            assert test_data_types[i] == test_result.type_name

    def test_06_get_values(self):
        
        test_data_date_start = [1694613014, 1694613014, 1695109889, None]
        test_data_date_end = [1694616614, 1694616614, None, 1695109889]
        test_data_type_id = [None, 1, None, None]
        expected_result_ammount = [12, 4, 1221, 1347]

        self.engine = db.create_engine("sqlite:///api/tests/test_db.db")
        crud = Crud(self.engine)

        for i, value in enumerate(test_data_date_end):
            result = crud.get_values(test_data_type_id[i], 
                                     test_data_date_start[i], 
                                     test_data_date_end[i])
            # what does the return look like ??
            
            assert expected_result_ammount[i] == len(result)
