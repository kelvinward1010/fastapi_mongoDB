from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import post, file



app = FastAPI()


origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
  
@app.get("/")
def root():
    return {"message": "Wellcome to my FastAPI with MongoDB"}

app.include_router(post.router)
app.include_router(file.router)