from fastapi import APIRouter, Query, Path, Body
from typing import Optional, List
from pydantic import BaseModel


router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"data": "Not found"}},
)

items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"}
]


# Pydantic model for data validation
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


class User(BaseModel):
    username: str
    full_name: Optional[str] = None


class Category(BaseModel):
    name: str
    slug: str


# Function parameters that are not path parameters, are "query" parameters.
# Both are default parameter here. We can call this route:
#   /items/
#   /items/?skip=0&limit=10
#   /items/?limit=20
#   /items/?skip=20
@router.get("/")
def all_items(skip: int = 0, limit: int = 10):
    return {"data": items_db[skip:skip+limit]}


# We can pass optional paramters
@router.get("/{id}")
def get_item(id: str, q: Optional[str] = None):
    return {"data": {"id": id, "title": "Product id " + str(id), q: q}}


# Bool types will be converted
# We can use:
#   /items/10?short=1
#   /items/10?short=True
#   /items/10?short=true
#   /items/10?short=on
#   /items/10?short=yes
@router.get("/{item_id}/available")
async def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return {"data": item}


# We can send data from a client/browser to our API as a request body.
# Request body is declared as parameter with type of data model.
@router.post("/")
async def create_item(item: Item):
    item_dict = item.dict()

    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})

    return {"data": item_dict}


# Request body + path + query parameters
# The function parameters will be recognized as follows:
#     If it is declared in the path, it will be used as a path parameter.
#     If it is of a singular type (like int, float, str, bool, etc) it will be interpreted as a query parameter.
#     If it is declared to be of the type of a Pydantic model, it will be interpreted as a request body.
@router.post("/{item_id}")
async def create_item_with_id(
    # Usually mixed parameter without value like item here will show error
    # Starting with * as first parameter, python will detect next parameters as kwargs
    *,
    # Path parameter can be validated with gt, ge, lt, le
    item_id: int = Path(..., title="The ID of the item to get", ge=0, le=1000),
    item: Item,
    # Multiple body parameter can be used and also any body parameter can be optional
    user: Optional[User] = None,
    # Singular values in body can be used and also with validation
    importance: int = Body(..., gt=0),
    q: Optional[str] = None
):
    item_dict = {"item_id": item_id, **item.dict(), "user": user,
                 "importance": importance}

    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})

    if q:
        item_dict.update({"q": q})

    return {"data": item_dict}


# If we have a single item body parameter,  FastAPI will then expect its body directly
# With body parameter embed, we expect a JSON with a key item category
@router.get("/categories")
async def get_categories(category: Category = Body(..., embed=True)):
    return {"data": {"category": category}}


# Query parameter with validation
@router.get("/query/test")
async def query_item(
    # query with validation
    material: Optional[str] = Query(None, max_length=10, min_length=2),
    # query with default value
    length: Optional[int] = Query(10),
    # query is required
    width: Optional[int] = Query(...),
    # query with multiple values, e.g, /items/?q=foo&q=bar
    color: Optional[List[str]] = Query(None),
    # query with details
    description: Optional[str] = Query(
        None,
        title="Query description",
        description="Query string for description",
        min_length=3,
        alias="summary"  # summary will be passed instead of description
    ),
):
    return {"data": {"length": length, "width": width, "material": material, "color": color, "description": description}}
