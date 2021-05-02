from enum import Enum
from fastapi import APIRouter

router = APIRouter()


class LangName(str, Enum):
    php = "php"
    python = "python"
    js = "js"


# We can use enum as predefined values for path params
@router.get("/lang/{lang_name}")
async def get_model(lang_name: LangName):
    print(lang_name)  # LangName.php
    print(lang_name.value)  # php

    # We can evaluate path parameter from enum class
    # i.e., we can compare it with the enumeration member in our created enum LangName
    if lang_name == LangName.php:
        return {"data": {"lang_name": lang_name, "message": f"{lang_name} is a wonderful backend language!"}}

    # Or we can evaluate the actual value directly
    if lang_name.value == "python":
        return {"data": {"lang_name": lang_name, "message": "python is the most powerful language for ML!"}}

    return {"data": {"lang_name": lang_name, "message": "js is has many more uses!"}}


# :path, tells it that the parameter should match any path
@router.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"data": {"file_path": file_path}}
