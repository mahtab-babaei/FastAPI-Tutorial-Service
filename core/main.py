from fastapi import FastAPI
import random

app = FastAPI()

names_list = [
    {"id": 1, "name": "John"},
    {"id": 2, "name": "Jane"},
    {"id": 3, "name": "Jack"},
    {"id": 4, "name": "Joe"},
    {"id": 5, "name": "June"},
]


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/names")
def retrieve_names_list():
    return names_list


@app.post("/names")
def create_name(name: str):
    name_obj = {"id": random.randint(6, 100), "name": name}
    names_list.append(name_obj)
    return name_obj


@app.get("/names/{name_id}")
def retrieve_name_detail(name_id: int):
    for name in names_list:
        if name["id"] == name_id:
            return name
    return {"message": "Name not found"}
