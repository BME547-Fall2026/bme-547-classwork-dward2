from mystery_math import complicated_formula


def do_math(item):
    x = item
    y = complicated_formula(x)
    add = x + y
    subtract = x - y
    multi = x * y
    divi = x / y
    z = complicated_formula(x)
    return [add, subtract, multi, divi, z]


def main():
    result_db = []
    my_list = [5, 10, 4, 13, -2, 14]
    for i in my_list:
        result = do_math(i)
        result_db.append(result)


if __name__ == "__main__":
    main()
