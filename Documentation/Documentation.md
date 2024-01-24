# Documentation API

## All important files

├── csv_application        
│   └── main.py    
├── rdb.test.db    
├── rdp   
│   ├── api    
│   │   ├── api_types.py    
│   │   ├── main.py     
│   ├── crud      
│   │   ├── crud.py     
│   │   ├── model.py      
│   ├── sensor        
│   │   └── reader.py       

> [!IMPORTANT]
> You either use the sensor/reader.py for adding data to the database,
> or the csv_application/main.py

## Information for each file:

### csv_application/main.py

Loading csv files into the database using the [Api](#rdpapimainpy). 

### rdb.test.db

This is the database for the whole application. 
When changing things in the [Model](#rdpcrudmodelpy).

### rdp/api/api_types.py

This is for displaying the data in the 'localhost:8080/api/...'.

### rdp/api/main.py

This has all the api functions which are calling the [Crud](#rdpcrudcrudpy) functions.

### rdp/crud/crud.py

This contains all the functions for interactions with the [Database](#rdbtestdb).

### rdp/crud/model.py

This contains the strukture of the database.

### rdp/sensor/reader.py

Adding data to the database on the start of the server. 