from fastapi import FastAPI

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
