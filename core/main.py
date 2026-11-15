import random
from typing import List
from fastapi import FastAPI, status, HTTPException, Query, Path, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
# from dataclasses import dataclass
from schemas import PersonCreateSchema, PersonResponseSchema, PersonUpdateSchema
from typing import List
from pydantic import BaseModel, EmailStr, field_serializer
from fastapi.encoders import jsonable_encoder
from database import Base, engine, get_db, Person
from sqlalchemy.orm import Session


class User(BaseModel):
    name: str
    email: EmailStr
    account_id: int
    number: float

    @field_serializer("number")
    def serialize_float(self, value):
        return round(value, 2)


user = User(name="mahtab", email="mahtab@gmail.com",
            account_id=1, number=80.03336665656656)
print(user.model_dump())
print(user.model_dump_json())
print(user.model_dump_json(indent=2))
print(jsonable_encoder(user))


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    Base.metadata.create_all(engine)
    yield
    print("Application shutdown")

app = FastAPI(lifespan=lifespan)

names_list = [
    {"id": 1, "name": "John"},
    {"id": 2, "name": "Jane"},
    {"id": 3, "name": "Jack"},
    {"id": 4, "name": "Joe"},
    {"id": 5, "name": "June"},
]


@app.get("/")
def root():
    content = {"message": "Hello World"}
    return JSONResponse(content=content, status_code=status.HTTP_202_ACCEPTED)


@app.get("/names", response_model=List[PersonResponseSchema])
def retrieve_names_list(
    q: str | None = Query(
        alias="search",
        description="It will be searched with the title you provided",
        default=None,
        max_length=50,
        pattern='^[^0-9]*$'
    ),
    db: Session = Depends(get_db)
):
    query = db.query(Person)

    if q:
        query = query.filter_by(name=q)

    result = query.all()
    # if q:
    #     result = [item for item in names_list if q.lower() in item["name"].lower()]
    return result


# @dataclass
# class Student:
#     name: str
#     age: int


@app.post("/names", response_model=PersonResponseSchema)
def create_name(request: PersonCreateSchema, db: Session = Depends(get_db)):
    # name_obj = {"id": random.randint(6, 100), "name": person.name}
    # names_list.append(name_obj)

    # return JSONResponse(content=name_obj, status_code=status.HTTP_201_CREATED)
    new_person = Person(name=request.name)
    db.add(new_person)
    db.commit()
    # db.refresh(new_person)
    return new_person


@app.get("/names/{name_id}", response_model=PersonResponseSchema)
def retrieve_name_detail(name_id: int = Path(title="Object id", description="The id of the name in names_list"), db: Session = Depends(get_db)):
    # for item in names_list:
    #     if item["id"] == name_id:
    #         return JSONResponse(content=item, status_code=status.HTTP_200_OK)
    person = db.query(Person).filter_by(id=name_id).one_or_none()
    if person:
        return person
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Name not found")


@app.put("/names/{name_id}", response_model=PersonResponseSchema)
def update_name_detail(request: PersonUpdateSchema, name_id: int = Path(), db: Session = Depends(get_db)):
    # for item in names_list:
    #     if item["id"] == name_id:
    #         item["name"] = person.name
    #         return JSONResponse(content=item, status_code=status.HTTP_200_OK)
    person = db.query(Person).filter_by(id=name_id).one()
    if person:
        person.name = request.name
        db.commit()
        db.refresh(person)
        return person
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Person not found")


@app.delete("/names/{name_id}")
def delete_name(name_id: int, db: Session = Depends(get_db)):
    # for item in names_list:
    #     if item["id"] == name_id:
    #         names_list.remove(item)
    person = db.query(Person).filter_by(id=name_id).one_or_none()
    if person:
        db.delete(person)
        db.commit()
        return JSONResponse(content={"detail": f"Name with ID {name_id} removed successfuly"}, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Name not found")


# @app.post("/upload_file")
# def upload_file(file: bytes = File(...)):
#     print(file)
#     return {"file size": len(file)}

@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    print(file.__dict__)
    return {"file_name": file.filename, "content_type": file.content_type, "file_size": len(content)}
