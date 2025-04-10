from fastapi import FastAPI
from routes.item_routes import router as item_router


app = FastAPI()
app.include_router(item_router, prefix="/items")


@app.get("/")
def root():
    return {"status": "OK"}
