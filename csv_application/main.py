import requests

url = "http://localhost:8080/api"

def read_csv(filename, address, device):
    x = requests.post(url + f'/add_location/?name={address}&address={address}')
    print(x)
    y = requests.post(url + f'/add_device/?name={device}&location_id=3')
    with open(filename) as file:
        data = file.read().splitlines()
        print(data[0])
        requests.post(url + f'/add_type/?type_id=30&type_name={data[0][2]}&type_unit=percent')
        requests.post(url + f'/add_type/?type_id=31&type_name={data[0][3]}&type_unit=celsius')
        body = data[1:]
        for line in body:
            pass

path = "/home/simonr/Documents/STD_Datensatz.csv" # input("Give absolute file path: ")
address = "HIRSCHENKOGEL" # input("Give the address of the thing: ")
device = "Messstation Stundendaten" # input("Give the Device name: ")
read_csv(path, address, device)
