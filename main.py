from fastapi import FastAPI

from enum import Enum

app = FastAPI()


class LangName(str, Enum):
    php = "php"
    python = "python"
    js = "js"


@app.get("/")
def index():
    return {"data": {"Hello world!"}}


@app.get("/about")
def about():
    return {"data": {"name": "DHN", "age": 35, "email": "php.chandan@gmail.com"}}


# If two routes may have same endpoint like below,
# the static one must be executed earlier
# Otherwise it will show error
@app.get("/blog/edit")
def blog():
    return {"data": {"title": "This must be executed before path parameter"}}


# Dynamic route
# {id} will be come from url
@app.get("/blog/{id}")
def blog(id: int):
    return {"data": {"id": id, "title": "Blog id " + str(id)}}


# We can use enum as predefined values for path params
@app.get("/lang/{lang_name}")
async def get_model(lang_name: LangName):
    print(lang_name)  # LangName.php
    print(lang_name.value)  # php

    # We can evaluate path parameter from enum class
    # i.e., we can compare it with the enumeration member in our created enum LangName
    if lang_name == LangName.php:
        return {"lang_name": lang_name, "message": f"{lang_name} is a wonderful backend language!"}

    # Or we can evaluate the actual value directly
    if lang_name.value == "python":
        return {"lang_name": lang_name, "message": "python is the most powerful language for ML!"}

    return {"lang_name": lang_name, "message": "js is has many more uses!"}


# :path, tells it that the parameter should match any path
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"data": {"file_path": file_path}}
