import base64
import requests

filename = "./images/esophagus1.jpg"

with open(filename, "rb") as image_file:
    b64_bytes = base64.b64encode(image_file.read())
# print(b64_bytes)
b64_string = str(b64_bytes, encoding='utf-8')
# print(b64_string)

server = "http://vcm-51170.vm.duke.edu"

out_dict = {"image": b64_string, "net_id": "daw74", "id_no": 2,
            "font_color": "white"}
r = requests.post(server+"/add_image", json=out_dict)
print(r.status_code)
print(r.text)

r = requests.get(server+"/get_image/daw74/2")
new_b64_string = r.text

image_bytes = base64.b64decode(new_b64_string)
with open("watermark.jpg", "wb") as out_file:
    out_file.write(image_bytes)
