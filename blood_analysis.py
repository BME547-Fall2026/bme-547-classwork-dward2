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
    

    
    
def controller():
    test_choice, test_value = user_input()
    print(test_choice, test_value)
    
    
controller()

    