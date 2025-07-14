from fastapi import FastAPI
from db import engine, Base
from models import Usuario, Curso, Leccion, Nota 
from routers.auth_routers import auth_routes

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router)


# Healthcheck
@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "message": "API is running smoothly"}
