from flask import Flask, request


app = Flask(__name__)


@app.route("/process_patient/<net_id>", methods=["POST"])
def function_to_break(net_id):
    """
    http://vcm-51170.vm.duke.edu:5000
    in_json = {"name": "David Ward",
               "heart_rates": [60, 64, 62],
               "email":  "daw74@duke.edu",
               "balance": 145.35,
               }
    Returns:

    """
    in_data = request.get_json()
    if type(in_data) is not dict:
        return "JSON input must be a dictionary, not a {}".format(type(in_data)), 400
    expected_keys = ["name", "heart_rates", "email", "balance"]
    for ex_key in expected_keys:
        if ex_key not in in_data:
            return "Key {} is missing.".format(ex_key), 400
    patient_name = in_data["name"]
    if type(patient_name) is not str:
        return "Patient name needs to be a string, not a {}".format(type(patient_name)), 400
    if patient_name.find(" ") < 0:
        first_name = ""
        last_name = patient_name
    else:
        first_name, last_name = patient_name.split(" ", 1)
    balance = in_data["balance"]
    if type(balance) not in [int, float]:
        return "Balance must be an integer or float.", 400
    balance = balance + 25.00
    heart_rates = in_data["heart_rates"]
    if type(heart_rates) is not list:
        return "Heart_rates should be a list, not a {}".format(type(heart_rates)), 400
    if len(heart_rates) == 0:
        average_heart_rate = 0
    else:
        total = 0
        for hr in heart_rates:
            if type(hr) not in [int, float]:
                return "Heart rates must be an integer or float.  You included a {}".format(hr), 400
            else:
                total += hr
        average_heart_rate = total / len(heart_rates)
    email = in_data["email"]
    if type(email) is not str:
        return "Email field must be a string", 400
    at_location = email.find("@")
    if at_location < 0:
        return "Email is missing @", 400
    patient_id = email[:at_location]
    domain = email[at_location+1:]
    if domain.find(".") < 0:
        return "No period between domain and top level", 400
    top_level = domain.split(".")[1]
    out_dict = {
        "first_name": first_name,
        "last_name": last_name,
        "new_balance": balance,
        "average_heart_rate": average_heart_rate,
        "net_id": patient_id,
        "domain": domain,
        "top_level": top_level
    }
    return out_dict


if __name__ == '__main__':
    app.run(port=5006)
