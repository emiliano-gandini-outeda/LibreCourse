from fastapi import FastAPI
from db import engine, Base
from models import Usuario, Curso, Leccion, Nota 
from routers import categories, auth_routers
import uvicorn
import os

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(categories.router)
app.include_router(auth_routers.router)


# Healthcheck
@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "message": "API is running smoothly"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)