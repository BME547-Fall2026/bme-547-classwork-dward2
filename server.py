from flask import Flask, request, jsonify
import database

app = Flask(__name__)


@app.route("/", methods=["GET"])
def server_status():
    return "Patient Monitoring Server is On"


@app.route("/add_patient", methods=["POST"])
def post_add_patient():
    """
    incoming data {"name": <str>, "mrn": <int>, "dob": <str>}
    """
    # Get input data
    in_data = request.get_json()
    # Call other functions to do the work
    result = validate_input_for_add_patient(in_data)
    if result is not True:
        return result, 400
    answer = database.process_new_patient(in_data)
    # Return a response
    return jsonify(answer), 200


def validate_input_for_add_patient(in_data):
    if type(in_data) is not dict:
        return "JSON data needs to be a dictionary."
    expected = {"name": str, "mrn": int, "dob": str}
    for ex_key in expected:
        if ex_key not in in_data:
            return "Key {} is missing".format(ex_key)
    for ex_key in expected:
        if type(in_data[ex_key]) is not expected[ex_key]:
            return "Key {} value is not {}".format(ex_key, expected[ex_key])
    return True



@app.route("/get_patient/<mrn>", methods=["GET"])
def get_get_patient(mrn):
    mrn = int(mrn)
    output = database.get_patient_for_server(mrn)
    return jsonify(output)


@app.route("/add_test", methods=["POST"])
def post_add_test():
    """
        {"mrn": <int>, "test_name": <str>, "test_value", <float>}
    """
    in_data = request.get_json()
    answer = database.add_test_to_patient(in_data["mrn"],
                                          in_data["test_name"],
                                          in_data["test_value"])
    return jsonify(answer)


if __name__ == "__main__":
    app.run()
