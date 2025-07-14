from fastapi import FastAPI
from db import engine, Base
from models import Usuario, Curso, Leccion, Nota 
from routers import categories, auth_routers

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(categories.router)
app.include_router(auth_routers.router)


# Healthcheck
@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "message": "API is running smoothly"}
