from fastapi import APIRouter, Depends

from app.dependencies import get_token_header

router = APIRouter(
    # we can prefix all with one
    prefix="/users",
    # tag will keep routes in group
    tags=["users"],
    # all the following routes will be depend upon this
    dependencies=[Depends(get_token_header)],
    responses={404: {"data": "Not found"}},
)


# We can also add specific tags
# then the route will be member of both groups
@router.get("/", tags=['customer'])
async def get_users():
    return {"data": [{"username": "DHN"}, {"username": "Sajib"}]}


@router.get("/me")
async def get_user_me():
    return {"data": {"name": "DHN", "age": 35, "email": "php.chandan@gmail.com"}}


@router.get("/{username}")
async def get_user(username: str):
    return {"data": {"username": username}}
