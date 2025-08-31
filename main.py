from fastapi import FastAPI
from src.api import main_router
from src.database import sync_engine, Base

app = FastAPI()

app.include_router(main_router)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=sync_engine)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

