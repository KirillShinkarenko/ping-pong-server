from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/ping")
async def ping():
    return {"message": "pong"}


@app.get("/ping/{ping_id}")
async def ping(ping_id: int):
    return {"message": f"pong {ping_id}"}
