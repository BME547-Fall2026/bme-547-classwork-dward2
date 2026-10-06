def calc_square_root(n):
    if type(n) is str:
        raise TypeError("Function expects a number as a parameter")
    if n < 0:
        raise ValueError("Function does not accept negative numbers.")

    try:
        print("Trying...")
        from my_calculator import sqrt
    except ModuleNotFoundError:
        print("Fixing...")
        from math import sqrt

    answer = sqxrt(n)
    return answer


def main():
    input_variable = 4
    try:
        answer = calc_square_root(input_variable)
    except ValueError:
        answer = calc_square_root(-input_variable)
    except TypeError:
        answer = calc_square_root(float(input_variable))
    except ModuleNotFoundError, ImportError:
        print("Check your file structure")
    except Exception as e:
        print(e)
        print(e.__dir__())
        # print(e.traceback())


if __name__ == "__main__":
    main()
"""
ERRORS
DIVBYZERO    x = 3 / 0\
TypeError  x = 3 + "Hello"
SyntaxError  if
FileNotFoundError    open("file.sldkjfls", 'r')
IndexError  x = [1, 2, 3]     x[6]

"""
