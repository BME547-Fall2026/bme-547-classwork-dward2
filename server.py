from flask import Flask, request, jsonify
import database

app = Flask(__name__)


@app.route("/", methods=["GET"])
def server_status():
    return "Patient Monitoring Server is On"


@app.route("/add_patient", methods=["POST"])
def post_add_patient():
    """
    incoming data {"name": <str>, "mnr": <int>, "dob": <str>}
    """
    # Get input data
    in_data = request.get_json()
    # Call other functions to do the work
    answer = database.process_new_patient(in_data)
    # Return a response
    return jsonify(answer)


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
