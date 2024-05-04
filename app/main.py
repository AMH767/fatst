from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

# If we use Alembic to handle our database migrations,
# we no longer need sqlalchemy to create the models for us in the initial stage (when we run the server for the first time)
# hence we would not need the code below
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

@app.get("/")
def root():
    return {"msg": "hello universe!!!!"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)