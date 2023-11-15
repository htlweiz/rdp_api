"""Module for Sending CSV Values to API."""

import pandas as pd
import requests


def send_data_to_api(device_id, data):
    """Send data to a specified API endpoint using HTTP PUT.

    Args:
        device_id (int): The device ID for the PUT request.
        data (dict): Dictionary representing the data to be sent.

    Returns:
        None
    """
    api_url = f'http://localhost:8080/api/value/{device_id}'
    response = requests.put(api_url, json=data)
    if response.status_code == 200:
        print(f"Data sent successfully for device {device_id}.")
    else:
        print(f"Failed to send data for device {device_id}. Status code: {response.status_code}")
        print(response.text)


def main():
    """Read CSV data, convert to dictionary, and send to API."""
    csv_file_path = 'api/csv_client/dataset_20231001T0000_20231031T2300.csv'
    device_id = 1

    df = pd.read_csv(csv_file_path)

    for i, row in df.iterrows():
        time = row['time']
        value = row['LT2']

        # Modified the data_to_send dictionary to include device_id
        data_to_send = {'time': time, 'value': value, 'type_id': 1}

        send_data_to_api(device_id, data_to_send)


if __name__ == "__main__":
    main()
