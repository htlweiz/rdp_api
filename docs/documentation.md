# Erweiterung des CRUD-Modells
Das CRUD-Modell wurde um folgende Tabellen erweitert: <br>
    - Device <br>
    - Room <br>
    - Location <br>


<img src="https://github.com/denisepostl/rdp_api/blob/main/docs/datamodel.png">

Dafür wurden zuerst im ```model.py``` die entsprechenden Anpassungen vorgenommen. SQLAlchemy ist ein ORM und bildet Objekte direkt in Tabellen ab. Um die ForeignKeys zu repräsentieren wird ```back_populates``` verwendet. ```back_populates``` gibt sozusagen die Gegenstelle an. Wird ```back_populates``` verwendet muss die Beziehung auf beiden Seiten angegeben werden. Damit die ID automatisch generiert wird wird ```autoincrement``` auf ```True``` gesetzt.

## Erstellen einer neuen Tabelle:

```python
class Device(Base):
    __tablename__ = "device"
```

## Definition des Foregn Key's

```python
    room_id: Mapped[int] = mapped_column(ForeignKey("room.id"), nullable=True)
```

## Definition der Gegenstelle:

```python
    room: Mapped["Room"] = relationship(back_populates="devices")
```

Um ein Device, Value, Room oder eine Location hinzuzufügen wurden entsprechende Anpassungen im ```crud.py``` vorgenommen. <br><br>
    - get_<elements>(Entries als Parameter) ... - retourniert die gesamten Daten einer Tabelle (Device, Value, Room, Location) <br><br>
    Retourniert die Liste der Entries (Alle Entries einer Tabelle):
```python
    stmt = select(Device)
    session.scalars(stmt).all()
``` 
<br>
    - get_<element>(Entries als Parameter) ... - retourniert anhand der eingegebenen ID nur einen bestimmten Entry einer Tabelle
<br><br>
Retourniert nur einen bestimmten Entry: <br>

```python
    stmt = select(Device).where(Device.id == id) # Auswahl eines Entries anhand der ID <br>
    session.scalars(stmt).one()
```

<br>
-update_<element>(Entries als Parameter) ... - ermöglicht es einen Entry zu aktualisieren.

<br>
<br>
Auswahl des Entries der aktualisiert werden soll:

```python 
stmt = select(Location).where(Location.id == location_id)
```
<br>
Übernahme der Änderung:

```python
session.add(db_location)
session.commit()
session.refresh(db_location)
```

-add_<element>(Entries als Parameter) ... - ermöglicht es einen neuen Entry hinzuzufügen.

<br>

Hinzufügen neuer Entries durch Übergabe der Parameter
```python
new_location = Location(name=location_name, city=city)
session.add(new_location)
session.refresh(new_room)
```

## Hinzufügen der Endpoints

Die implementierten Funktionen im CRUD wurden jeweils für die Erweiterung der API aufgerufen.

```python
def post/get/put_<element>(parameter - Werte, die hinzugefügt/aktualisiert/zurückgegeben werden sollen):
    # Aufruf der entsprechenden Funktion im CRUD-Modul
    crud.add_/get_/update_/...(parameter)
```

API-Operationen

```python
@app.get("/value/") # Alle Entries retournieren
@app.get("/value/{id}") # Einen spezifischen Entry anhand der ID retournieren
@app.put("/value/{id}/") # Einen Entry über die ID updaten
@app.post("/value/") # Einen neuen Entry hinzufügen
```

Anpassungen im ```api_types.py```
Die API Types wurden entsprechend erweitert, die in Verbindung mit den API-Endpunkten stehen.

```python
def get_/post_/put_/...(parameter - Werte, die hinzugefügt/aktualisiert/zurückgegeb werden sollen) -> List[ApiTypes.Value]:

class DeviceNoID(BaseModel):
    name: str
    .
    .
    . 

class Device(DeviceNoID):
    id: int 
    . 
    . 
    .
```

Anpassungen im ```reader.py```
Um die Testdatenbank entsprechend mit Testdaten zu beladen wurden entsprechende Funktion vom crud aufgerufen und mit Testdaten befüllt.

```python 
def _run(self) -> None:
    .
    .
    .
    
    self._crud.add_...(Parameter der zu hinzufügenden Werte)
    . 
    . 
    .
```

# CSV Client
Dieses Programm ermöglicht die Übermittlung von Daten aus CSV-Dateien an einen API-Endpunkt mithilfe einer Flask-basierten Benutzeroberfläche. Es wurde entwickelt, um den Benutzern das Hochladen von CSV-Dateien, das Hinzufügen neuer Geräte und das Abrufen vorhandener Geräte über eine Webanwendung zu erleichtern.

## Hauptkomponenten

### CSV-Datenverarbeitung

Die Klasse `APIDataSender` enthält zwei Hauptmethoden:

- `read_csv_data(csv_file, device_id)`: Liest Daten aus einer CSV-Datei und formatiert sie für die API.
- `send_data_to_api(data, device_id)`: Sendet formatierte Daten an die API-Endpunkte.

### Flask-Webanwendung

Es wurde eine Flask-App erstellt, die folgende Routen bereitstellt:

- `/`: Hauptseite für das Hochladen von CSV-Dateien und die Datenübermittlung an die API.
- `/upload_file`: Routen für das Hochladen von Dateien.
- `/add_device`: Routen für das Hinzufügen neuer Geräte und Übermittlung der zugehörigen Daten an die API.
- `/get_devices`: Routen für das Abrufen vorhandener Geräte von der API.

### Globale Variablen

- `api_url`: Globale Variable für den API-Endpunkt zur Übermittlung von Daten.
- `api_url_device`: Globale Variable für den API-Endpunkt zum Hinzufügen von Geräten.

## Fluss des Programms

1. Benutzer lädt eine CSV-Datei über die Webanwendung hoch.
2. Die Daten werden von der `APIDataSender`-Klasse verarbeitet und an die API gesendet.
3. Die Benutzeroberfläche ermöglicht das Hinzufügen neuer Geräte und das Abrufen vorhandener Geräte.

## Fehlerbehandlung

Fehler bei der Datenübermittlung an die API werden abgefangen und ausgegeben.

## Verwendung

### Hochladen von CSV-Dateien

1. Hochladen der Datei in der Hauptseite der Webanwendung.
2. Auswahl einer CSV-Datei und anschließend über den upload button hochladen.

### Hinzufügen neuer Geräte

1. Einfügen erforderlicher Daten in die Felder.
2. Hinzufügen des devices und der values. Die device_id wird automatisch mit den values im csv-file verknüpft.

### Abrufen vorhandener Geräte

1. Über den Button Get Devices können vorhandene Geräte retourniert werden.

## Voraussetzungen

- Flask
- requests

Sicherstellen, dass die API-Endpunkte korrekt funktionieren.

## Ausführung

Anschließend kann das Programm mittels ```python app.py``` ausgeführt werden.

## Anpassung

Die globalen Variablen `api_url` und `api_url_device` können bei Bedarf angepasst werden. 
