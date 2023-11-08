import pandas as pd
import requests
import time
from datetime import datetime


class FileUploader():

    """def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FileUploader, cls).__new__(cls)
        return cls.instance"""

    def __init__(self, csv_file) -> None:

        self.csv_file = csv_file
        self.api_url = 'http://127.0.0.1:8888/'
        self.df_content = pd.DataFrame(pd.read_csv(csv_file, sep=','))
        self.devices = list(dict.fromkeys(self.df_content.device))

        self.checkCSV()

        response = requests.get(f"{self.api_url}")
        if response.status_code != 200:
            raise Exception(f"Hello person, there's a {response.status_code}"
                  f"error with your request")

    def checkCSV(self):

        content = pd.read_csv(self.csv_file, sep=',')

        df_content = pd.DataFrame(content)

        if not set(['time', 'device', 'Luftfäuchte', 'Temperatur',
                    'Luftdruck']).issubset(df_content.columns):
            raise Exception('CSV file is not formatted correctly')
        return True

    def uploadDevice(self):

        for device in self.devices:
            # add device
            API_ENDPOINT = self.api_url + "api/device/" + str(device) + "/"
            data = {
                'name': str('device' + str(device)),
                'room_id': 1
            }

            response = requests.put(url=API_ENDPOINT, json=data)
            pastebin_url = response.text
            print("The pastebin URL is: %s" % pastebin_url)
            if response.text == 'Internal Server Error':
                raise Exception('Device could not be uploaded')

            time.sleep(1)

    def uploadValue(self):

        # temp => 0
        # hum => 1
        # psi => 2

        API_ENDPOINT = self.api_url + "api/value/"

        # could make this into a function that gets the current types
        value_types = ['Temperatur', 'Luftfäuchte', 'Luftdruck']

        for index, row in self.df_content.iterrows():

            for i, type in enumerate(value_types):
                print(row[type])

                value = self.checkValue(type, row[type])
                print(value)

                if (value != -999):
                    time_ = int(datetime.fromisoformat(row['time']).timestamp())
                    print(time_)
                    data = {
                        'value_type_id': i,
                        'device_id': row['device'],
                        'time': time_,
                        'value': value
                    }
                    print(data)

                    response = requests.post(url=API_ENDPOINT, json=data)
                    if response.text == 'Internal Server Error':
                        raise Exception('Value could not be uploaded')

                    time.sleep(1)

    def checkValue(self, type, value):

        if type == "Temperatur":
            if (value < -30 and value > 50):
                raise -999
            else:
                return value
        elif type == "Luftfäuchte":
            if (value < 0 and value > 100):
                raise -999
            else:
                return value
        elif type == "Luftdruck":
            if (value < 500 and value > 1020):
                raise -999
            else:
                return value
        else:
            raise Exception("No value found")

    def getTypes(self) -> list:

        response = requests.get(self.api_url + "api/type/").json()
        types = []
        for piece in response:
            types.append(piece['type_name'])
        return types
