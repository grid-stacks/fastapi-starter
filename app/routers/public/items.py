from fastapi import APIRouter
from typing import Optional

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
    return item
