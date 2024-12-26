"""
Main app start
"""

from fastapi import FastAPI
from app.services.ex_collection1 import router as ex_collection1_router

app = FastAPI()

app.include_router(ex_collection1_router, prefix="/milvus", tags=["Milvus"])

@app.get("/")
async def root():
    """
    Default
    """
    return {"message": "Welcome to the Milvus API"}
