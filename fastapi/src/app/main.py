from fastapi import FastAPI

from .schemas import KeyValueIn, KeyValueOut

app = FastAPI()

db = {}


@app.get("/")
def root():
    return {"hello": "world"}


@app.post("/add", response_model=KeyValueOut)
def add_value(req: KeyValueIn):
    if req.key in db:
        resp = KeyValueOut(status="key_exists", **req.dict())
    else:
        db[req.key] = req.value
        resp = KeyValueOut(**req.dict())
    return resp
