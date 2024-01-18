from flask import Flask, render_template, request, redirect, url_for, session
import csv
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'key'
api_url = "http://localhost:8080/api/value/"
api_url_device = "http://localhost:8080/api/device/"

class APIDataSender():
    """
    Class for sending data to API.

    Methods:
    --------
    read_csv_data(csv_file: str, device_id: int)
        Reads data from a CSV file and formats it for API consumption.

        Parameters:
        ----------
        csv_file : str
            Path to the CSV file.
        device_id : int
            Device ID associated with the data.

        Returns:
        -------
        List[Dict[str,[int, float]]]
            Formatted data ready for API consumption.


    send_data_to_api(data: List[str,[int,float]]], device_id: int)
        Send data to the API.

        Parameters:
        -----------
        data : List[Dict[str, [int,float]]]
            Formatted data to be sent to API.
        device_id : int
            Device ID assaciated with the data.

        Returns:
        --------
        None
    """

    def read_csv_data(self, csv_file, device_id):
        """
        Reads data from a CSV file and formats it for API consumption.

        Parameters:
        ----------
        csv_file : str
            Path to the CSV file.
        device_id : int
            Device ID associated with the data.

        Returns:
        -------
        List[Dict[str,[int, float]]]
            Formatted data ready for API consumption.
        """
        data = []

        with open(csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                time_str = row['time']
                time_obj = datetime.fromisoformat(time_str)
                value_time = int(time_obj.timestamp())

                value_temp = float(row['T'])
                value_pg = float(row['Pg'])
                value_a = float(row['a'])

                data.append({
                    "value_time": value_time,
                    "value_type_id": 0,
                    "device_id": device_id,
                    "value_value": value_temp,
                })

                data.append({
                    "value_time": value_time,
                    "value_type_id": 1,
                    "device_id": device_id,
                    "value_value": value_pg
                })

                data.append({
                    "value_time": value_time,
                    "value_type_id": 2,
                    "device_id": device_id,
                    "value_value": value_a
                })
        return data

    def send_data_to_api(self, data, device_id):
        """
         Send data to the API.

        Parameters:
        -----------
        data : List[Dict[str, [int,float]]]
            Formatted data to be sent to API.
        device_id : int
            Device ID assaciated with the data.

        Returns:
        --------
        None
        """
        for item in data:
            try:
                response = requests.post(
                    api_url,
                    params={
                        "value_time": item["value_time"],
                        "value_type_id": item["value_type_id"],
                        "device_id": device_id,
                        "value_value": item["value_value"],
                    }
                )
                response.raise_for_status()
                print(f"Data sent for value_time {item['value_time']} successfully!")
            except requests.exceptions.RequestException as e:
                print(f"Error sending data for value_time {item['value_time']}: {str(e)}")

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Flask route for the index page.

    Returns:
    -------
    render_template
        HTML template with success_message and fetched_values.
    """

    success_message = None
    fetched_values = None

    if request.method == 'POST':
        data_sender = APIDataSender()
        uploaded_file = request.files['file']

        if uploaded_file.filename != '':
            file_path = f"{uploaded_file.filename}"
            uploaded_file.save(file_path)
            session['file_path'] = file_path

            try:
                data = data_sender.read_csv_data(file_path)
                data_sender.send_data_to_api(data, device_id=None)
            except Exception as e:
                success_message = f"Fehler beim Senden der Daten: {str(e)}"
        else:
            success_message = "Bitte laden Sie zuerst eine Datei hoch."

    return render_template('index.html', success_message=success_message, fetched_values=fetched_values)

@app.route('/upload_file', methods=['POST'])
def upload_file():
    """
    Flask route for uploading a file.

    Returns:
    -------
    render_template
        HTML template with success_message and fetched_values.
    """

    uploaded_file = request.files['file']

    if uploaded_file.filename != '':
        file_path = f"{uploaded_file.filename}"
        uploaded_file.save(file_path)
        session['file_path'] = file_path
        return redirect(url_for('index'))

    return render_template('index.html', success_message=None, fetched_values=None)


@app.route('/add_device', methods=['POST'])
def add_device():
    """
    Flask route for adding a device.

    Returns:
    --------
    render_template
        HTML template with success_message.

    """
    try:
        device_data = {
            "name": request.form['name'],
            "device": request.form['device'],
            "postalCode": int(request.form['postal_code']),
            "city": request.form['city'],
            "room_id": int(request.form['room_id']),
        }

        response = requests.post(api_url_device, json=device_data)
        response.raise_for_status()

        if response.status_code == 200:
            new_device_id = response.json().get('id')
            success_message = "Device and Values added successfully!"

            data_sender = APIDataSender()
            file_path = session.get('file_path')
            if file_path:
                data = data_sender.read_csv_data(file_path, device_id=new_device_id)

                data_sender.send_data_to_api(data, device_id=new_device_id)

        else:
            success_message = f"Error adding device and values: {response.text}"

    except requests.exceptions.RequestException as e:
        success_message = f"Error adding device and values: {str(e)}"

    return render_template('index.html', success_message=success_message)

@app.route('/get_devices', methods=['GET'])
def get_devices():
    """
    Flask route for fetching devices from the API.

    Returns:
    --------
    render_template
        HTML template with fetched_devices.

    """
    try:
        response = requests.get(api_url_device)
        response.raise_for_status()
        fetched_devices = response.json()

    except requests.exceptions.RequestException as e:
        fetched_devices = []
        print(f"Error fetching devices from API: {str(e)}")

    return render_template('index.html', fetched_devices=fetched_devices)

if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host='192.168.1.20') - for hosting it on special IP