from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return "Hello world!"


@app.get("/about")
def about():
    return {"data": {"name": "DHN", "age": 35, "email": "php.chandan@gmail.com"}}
