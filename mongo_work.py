from pymongo import MongoClient

uri = "mongodb+srv://bme547_class:db_demo@bme547.ba348.mongodb.net/"

client = MongoClient(uri)
client.admin.command("ping")
database = client["db_demo"]
collection = database["reviews"]


# CRUD

def create_review():
    entry = {"Reviewer": "David Ward",
             "Type": "Movie",
             "Title": "Lone Star",
             "Genre": "Mystery"}
    answer = collection.insert_one(entry)
    print(type(answer))
    print(answer)


def retrieve_review():
    entry = collection.find_one({"Title": "The Dark Knight"})
    print(type(entry))
    print(entry)


def retrieve_many_reviews():
    # genres = collection.distinct("Genre")
    # print(genres)
    entries = collection.find({"rating": {"$gte": 2}})
    print(type(entries))
    print(entries)
    for entry in entries:
        print(entry)


def update_review():
    entry = collection.find_one({"Watcher": "David Ward"})
    entry["Reviewer"] = "David Ward"
    entry.pop("Watcher")
    collection.replace_one({"_id": entry["_id"]}, entry)


def add_rating():
    entry = collection.find_one({"Title": "The Dark Knight"})
    entry["rating"] += 1
    collection.replace_one({"_id": entry["_id"]}, entry)


def delete_review():
    entry = collection.find_one({"Name": "The American President"})
    print(entry)
    answer = collection.delete_one({"Name": "The American President"})
    print(type(answer))
    print(answer)
    # collection.delete_many({"Type": "Songs"})


def main():
    # create_review()
    # retrieve_review()
    # retrieve_many_reviews()
    # update_review()
    # retrieve_many_reviews()
    # add_rating()
    # retrieve_review()
    delete_review()


if __name__ == "__main__":
    main()