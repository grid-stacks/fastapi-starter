from fastapi import APIRouter

router = APIRouter(
    prefix="/blogs",
    tags=["blogs"],
    responses={404: {"data": "Not found"}},
)


# If two routes may have same endpoint like below,
# the static one must be executed earlier
# Otherwise it will show error
@router.get("/edit")
def blog():
    return {"data": {"title": "This must be executed before path parameter"}}


# Dynamic route
# {id} will be come from url
@router.get("/{id}")
def blog(id: int):
    return {"data": {"id": id, "title": "Blog id " + str(id)}}
