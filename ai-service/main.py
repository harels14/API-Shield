from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message" : "Working"}


@app.get("/clean")
def clean():
    return {"message" : "cleaned"}




