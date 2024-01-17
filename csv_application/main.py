import requests
from datetime import datetime, timezone

url = "http://172.31.182.118:8080/api"

def read_csv(filename, address, device):
    location_response = requests.post(url + f'/add_location/?name={address}&address={address}')
    location_id = 0

    if location_response.status_code == 200 and location_response.text:
        location_id = location_response.text
    else:
        # Handle error, raise an exception, or return an error response
        print("Error adding location:", location_response.text)
        return

    device_response = requests.post(url + f'/add_device/?name={device}&location_id={location_id}')
    device_id = 0

    if device_response.status_code == 200 and device_response.text:
        device_id = device_response.text
    else:
        # Handle error, raise an exception, or return an error response
        print("Error adding device:", device_response.text)
        return

    data = []
    with open(filename) as file:
        l = file.read().splitlines()
        for line in l:
            line = line.strip().split(',')
            data.append(line)
        print(data[1])
        requests.post(url + f'/add_type/?type_id=1&type_name={data[0][2]}&type_unit=percent')
        requests.post(url + f'/add_type/?type_id=2&type_name={data[0][3]}&type_unit=celsius')
        body = data[1:]
        for line in body:
            time_format = "%Y-%m-%dT%H:%M%z"

            dt_object = datetime.strptime(line[0], time_format)
            timestamp = int(dt_object.timestamp())

            requests.post(url + f"/add_value/?value_time={timestamp}&value_type={1}&value_value={int(line[2].split('.')[0])}&value_device={device_id}")
            requests.post(url + f"/add_value/?value_time={timestamp}&value_type={2}&value_value={int(line[3].split('.')[0])}&value_device={device_id}")

path = input("Give absolute file path: ")
address = input("Give the address of the thing: ")
device = input("Give the Device name: ")
read_csv(path, address, device)
