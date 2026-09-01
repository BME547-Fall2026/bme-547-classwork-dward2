def user_input():
    print("Blood Analysis")
    print("Enter test type")
    print("1 - HDL")
    print("2 - LDL")
    print("3 - Total")
    test_choice = input("Enter the test number: ")
    test_value = input("Enter the test result: ")
    return test_choice, test_value
    
    
def convert_str_to_float(input_value):
    number = float(input_value)
    return number
    

def HDL_analysis(HDL_value):
    if HDL_value >= 60:
        answer = "Normal"
    elif 40 <= HDL_value < 60:
        answer = "Borderline Low"
    else:
        answer = "Low"
    return answer

def output_results(test_name, test_value, test_result):
    print("For a {} of value {}, the result is {}.".format(test_name, test_value, test_result))  
    
    
    
def controller():
    test_choice, test_value = user_input()
    test_value = convert_str_to_float(test_value)
    if test_choice == "1":
        result = HDL_analysis(test_value)
        test_name = "HDL"
    output_results(test_name, test_value, result)

    
    
    
controller()

    