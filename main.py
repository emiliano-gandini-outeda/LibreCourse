from fastapi import FastAPI
from .db import engine, Base
from . import models 

app = FastAPI()

Base.metadata.create_all(bind=engine)

