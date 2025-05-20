from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.item_routes import router as item_router

# crate the FastAPI app
app = FastAPI()

# configure CORS rather permissively
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# bring in the item routes
app.include_router(item_router, prefix="/items")


# add a simple health check endpoint
@app.get("/")
def root():
    return {"status": "OK"}
