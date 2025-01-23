from faker import Faker
import json
import random

faker = Faker()


def generate_data():
    users = [{"id": i, "name": faker.name(), "email": faker.email()}
             for i in range(1, 10001)]
    posts = [{"id": i, "title": faker.sentence(), "content": faker.text(
    ), "author_id": random.randint(1, 10000)} for i in range(1, 10001)]
    comments = [{"id": i, "text": faker.text(), "author_id": random.randint(
        1, 10000), "post_id": random.randint(1, 10000)} for i in range(1, 10001)]
    tags = [{"id": i, "name": faker.word()} for i in range(1, 10001)]
    return {"users": users, "posts": posts, "comments": comments, "tags": tags}


data = generate_data()

with open("test_data.json", "w") as file:
    json.dump(data, file)
