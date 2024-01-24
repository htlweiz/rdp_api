import requests
import pandas
import os
from flask import Flask, render_template, request, redirect, url_for
from dateutil import parser


app = Flask(__name__)
UPLOAD_FOLDER = 'files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    """
    Render the index page of the web application.

    This function responds to the root URL and is responsible for
    displaying the initial file upload form to the user.

    Returns:
        Output of the rendering function for 'index.html'.
    """
    return render_template('index.html')


@app.route("/", methods=['POST'])
def upload_files():
    """
    Handle the file upload and initiate data processing.

    This function is called when a POST request is made to the root URL.
    It saves the uploaded file to the configured UPLOAD_FOLDER and
    calls the send_data function to process and send the file's data.

    Returns:
        A redirect response to the index URL.
    """
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(
            app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
        send_data(file_path)
    return redirect(url_for('index'))


def send_data(file_path):
    """
    Process the CSV data and send it to the designated API endpoint.

    This function reads a CSV file from the given file path, extracts
    each row, and sends the data to an API endpoint after processing.
    The function prints the status code of each POST request to the console.

    Args:
        file_path (str): The path to the CSV file that has been uploaded.

    Returns:
        None
    """
    types = requests.get("http://localhost:8080/api/type/").json()
    required_type_name = "Temperature"
    type_id = None

    for item in types:
        if item['type_name'] == required_type_name:
            type_id = item['id']
            break

    url = "http://localhost:8080/api/value/"
    csv_data = pandas.read_csv(file_path)
    for _, row in csv_data.iterrows():
        datetime_obj = parser.parse(row.iloc[0])
        epoch_time = int(datetime_obj.timestamp())
        data = {
            'value_type': type_id,
            'value_time': int(epoch_time),
            'value_value': float(row.iloc[2]),
            'device_id': int(row.iloc[1]),
        }
        res = requests.post(url, params=data)
        print(res.status_code)


if __name__ == "__main__":
    app.run(debug=True)
