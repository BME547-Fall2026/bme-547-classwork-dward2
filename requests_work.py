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


def main():
    get_work()


if __name__ == "__main__":
    main()
