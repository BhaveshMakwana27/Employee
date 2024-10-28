from fastapi import FastAPI
import routes
import auth
from database import engine
import models

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(routes.route)
app.include_router(auth.route)