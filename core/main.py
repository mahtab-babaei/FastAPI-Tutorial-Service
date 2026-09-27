import random
from fastapi import FastAPI, status, HTTPException, Query, Path, Form, Body, File, UploadFile
from fastapi.responses import JSONResponse

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
    content = {"message": "Hello World"}
    return JSONResponse(content=content, status_code=status.HTTP_202_ACCEPTED)


@app.get("/names")
def retrieve_names_list(q: str | None = Query(alias="search", description="It will be searched with the title you provided", default=None, max_length=50, regex='^[^0-9]*$')):
    result = names_list
    if q:
        result = [item for item in names_list if q.lower()
                  in item["name"].lower()]
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)


@app.post("/names")
def create_name(name: str = Body(embed=True)):
    name_obj = {"id": random.randint(6, 100), "name": name}
    names_list.append(name_obj)
    return JSONResponse(content=name_obj, status_code=status.HTTP_201_CREATED)


@app.get("/names/{name_id}")
def retrieve_name_detail(name_id: int = Path(title="Object id", description="The id of the name in names_list")):
    for item in names_list:
        if item["id"] == name_id:
            return JSONResponse(content=item, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Name not found")


@app.put("/names/{name_id}")
def update_name_detail(name_id: int = Path(), name: str = Form()):
    for item in names_list:
        if item["id"] == name_id:
            item["name"] = name
            return JSONResponse(content=item, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Name not found")


@app.delete("/names/{name_id}")
def delete_name(name_id: int):
    for item in names_list:
        if item["id"] == name_id:
            names_list.remove(item)
            return JSONResponse(content={"detail": f"Name with ID {name_id} removed successfuly"}, status_code=status.HTTP_200_OK)
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
