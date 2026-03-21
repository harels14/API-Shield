from fastapi import FastAPI
from model import second_layer_clean

app = FastAPI()


@app.get("/")
def root():
    return {"message" : "Working"}


@app.get("/clean")
def clean():
    return {"message" : "cleaned"}


@app.get("/verify")
def verify(text: str):
    return second_layer_clean(text)




