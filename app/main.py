from fastapi import FastAPI

from app.routers.public import users, blogs, items, others


app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)
app.include_router(blogs.router)


# It's possible to include the same router multiple times with different prefix
#  Then we can expose same API under different prefixes, e.g. /api/v1 and /api/latest
app.include_router(
    others.router,
    prefix="/settings",
    tags=["settings"],
    responses={404: {"data": "Not found"}}
)
app.include_router(
    others.router,
    prefix="/others",
    tags=["others"],
    responses={404: {"data": "Not found"}}
)


@app.get("/")
def index():
    return {"data": {"Hello world!"}}
