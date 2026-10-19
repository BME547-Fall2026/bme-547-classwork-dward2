import requests

server = "https://api.github.com"


def get_work():

    r = requests.get(server + "/repos/dward2/bme547/branches")

    print(r)
    print(type(r))
    print(r.status_code)
    print(r.text)

    if r.status_code != 200:
        return "Didn't work"
    answer = r.json()
    print(type(answer))

    for branch in answer:
        print(branch["name"])


def post_work():
    server = "http://vcm-51170.vm.duke.edu:5000"

    out_json = {
                "name": "David Ward",
                "net_id": "daw74",
                "e-mail": "david.a.ward@duke.edu"
                }

    r = requests.post(server + "/student", json=out_json)
    print(r.status_code)
    print(r.text)


def get_student_count():
    server = "http://vcm-51170.vm.duke.edu:5000"
    r = requests.get(server + "/list")
    print(r.status_code)
    print("Number of students: {}".format(len(r.json())))


def main():
    # get_work()
    # post_work()
    get_student_count()


if __name__ == "__main__":
    main()
