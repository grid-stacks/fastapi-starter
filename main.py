from fastapi import FastAPI

app = FastAPI()


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
