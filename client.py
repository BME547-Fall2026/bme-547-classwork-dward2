import requests

server = "http://127.0.0.1:5000"

r = requests.get(server + "/")
print(r.status_code)
print(r.text)

out_json = {"name": "Ann Ables",
            "mrn": 123,
            "dob": "1/1/2000"}
r = requests.post(server + "/add_patient", json=out_json)
print(r.status_code)
print(r.text)

r = requests.get(server + "/get_patient/145")
print(r.status_code)
print(r.text)
print(r.json())

out_json = {"mrn": 123,
            "test_name": "HDL",
            "test_value": 62.1}
r = requests.post(server + "/add_test", json=out_json)
print(r.status_code)
print(r.text)
x = r.json()
print(x)
