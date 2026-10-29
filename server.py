from flask import Flask, request, jsonify
import database

app = Flask(__name__)


@app.route("/", methods=["GET"])
def server_status():
    """ A GET route to indicate that the server is active.

    This route returns a string in response to the request indicating that the
    server is active.  This is intended to allow the user know if the other
    functionality of the server is available.

    :return:
    """
    return "Patient Monitoring Server is On"


@app.route("/add_patient", methods=["POST"])
def post_add_patient():
    """ Implement POST route to add patient to database

    This function implements the /add_patient route of the server.  This POST
    route receives JSON input in the form of a dictionary:

        {
            "name": <str>,
            "mrn": <int>,
            "dob": <str>
        }

    The function calls a helper function to validate that the needed keys
    exist in the input dictionary and that the corresponding values are of the
    correct data type.  If the validation fails, a message about the error is
    returned as part of a 400 status code response.  If validation passes, the
    data is sent to the databae module to be added to the database and a
    successful 200 status code response is returned.

    Returns:
        str, int: String with outcome of request and an integer containing the
                  status code (200 for successful addition of patient, 400 if
                  there was a problem with the incoming data).
    """
    # Get input data
    in_data = request.get_json()
    # Call other functions to do the work
    expected = {"name": str, "mrn": int, "dob": str}
    result = generic_validate_input(in_data, expected)
    if result is not True:
        return result, 400
    answer = database.process_new_patient(in_data)
    # Return a response
    return jsonify(answer), 200


def generic_validate_input(in_data, expected):
    """ Validates keywords and data types of dictionary inputs

    This helper function is called by a flask handler function to validate that
    the keywords and data types sent to the server are those that were
    expected.  If an expected keyword is missing, or a value data types does
    not match the expected, an error message is returned.  If the keys and data
    types do match, True is returned.

    Args:
        in_data (dict): data received by the server to be validated
        expected (dict): keys are the keywords that are expected in the input
                         dictionary and the values are appropriate data type
                         that should exist for the value of the keyword in the
                         input.

    Returns:
        bool or str:  True if expected keys and data types are found, else a
                      string with an error message
    """
    if type(in_data) is not dict:
        return "JSON data needs to be a dictionary."
    for ex_key in expected:
        if ex_key not in in_data:
            return "Key {} is missing".format(ex_key)
    for ex_key in expected:
        if type(in_data[ex_key]) is not expected[ex_key]:
            return "Key {} value is not {}".format(ex_key, expected[ex_key])
    return True


@app.route("/get_patient/<mrn>", methods=["GET"])
def get_get_patient(mrn):
    """ Implement GET route for getting patient information

    This function implements the /get_patient/<mrn> route of the server.
    This route uses a variable URL in which to receive the medical record
    number of the patient.  The mrn is contained in a string from the variable
    URL.  This string is sent to a helper function that will either convert the
    mrn from a string to an integer or will return an error message.  If an
    error message is returned, this function will return that message as a
    response along with a 400 status code.  If the mrn is returned as an
    integer, that integer is used as the parameter to the
    database.get_patient_for_server function.  The result of this function call
    is returned to the requestor.

    Args:
        mrn (str): portion of the variable URL containing the patient medical
                    record number

    Returns:
        str:  patient information
        int:  status code
    """
    validated_mrn = validate_get_patient_mrn(mrn)
    if type(validated_mrn) is not int:
        return validated_mrn, 400
    output = database.get_patient_for_server(validated_mrn)
    return jsonify(output), 200


def validate_get_patient_mrn(mrn):
    """ Verifies that string contains a valid medical record number

    The purpose of this function is to determine if the input string contains
    an integer that is a valid medical record number.  First, the attempt is
    made to convert the string to an integer.  If it fails as indicated by the
    raising of a ValueError, the function returns a string error message.
    If the conversion is successful, a database function is called to check if
    the medical record number exists in the database.  If it does not, an
    error message is returned.  If it does, the integer mrn is returned.

    Args:
        mrn (str): string to be evaluated for whether it contains a valid mrn

    Returns:
        int or str:  Integer of medical record number if it exists in database,
                     else a string with an error message if the input string
                     does not contain a valid mrn
    """
    try:
        mrn = int(mrn)
    except ValueError:
        return "MRN must be an integer"
    answer = database.get_patient_by_mrn(mrn)
    if answer is None:
        return "MRN of {} does not exist".format(mrn)
    return mrn


@app.route("/add_test", methods=["POST"])
def post_add_test():
    """ Implement POST route for adding test data to a patient record

    This function implements the /add_test route of the server.  This POST
    route receives JSON input in the form of a dictionary:

        {
            "mrn": <int>,
            "test_name": <str>,
            "test_value": <float>
        }

    It contains the medical record number of the patient for whom the test
    belongs, the name of the test, and the test result.  This function
    validates the received data and returns an error message if the input
    data does not meet expectations.  If the input data is valid, the
    database is queried to see if the mrn exists in the database.  If not,
    an error message is returned.  If the mrn does exist, the
    database.add_test_to_patient function is called and sent the information.

    Returns:
        str, int:  message indicating either the success or failure of the
                   request and a status code (200 for success, 400 for error)
    """

    in_data = request.get_json()
    expected = {"mrn": int, "test_name": str, "test_value": float}
    result = generic_validate_input(in_data, expected)
    if result is not True:
        return result, 400
    exists = database.get_patient_by_mrn(in_data["mrn"])
    if exists is None:
        return "MRN of {} does not exist".format(in_data["mrn"]), 400
    answer = database.add_test_to_patient(in_data["mrn"],
                                          in_data["test_name"],
                                          in_data["test_value"])
    return jsonify(answer), 200


@app.route("/get_all_mrns", methods=["GET"])
def get_get_all_mrns():
    all_mrns = database.get_all_mrns()
    return jsonify(all_mrns), 200


if __name__ == "__main__":
    app.run()
