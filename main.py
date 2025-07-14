from fastapi import FastAPI
from db import engine, Base
from models import Usuario, Curso, Leccion, Nota 

app = FastAPI()

Base.metadata.create_all(bind=engine)

