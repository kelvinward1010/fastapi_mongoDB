from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from .routes import post, file, user, auth, comment, like



app = FastAPI()


origins = ['*', 'https://www.google.com']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
  
@app.get("/", tags=["Welcome to API Server"], response_class=HTMLResponse)
def welcome():
    return """
        <html>
            <head>
                <title>Wellcome to my FastAPI with MongoDB</title>
            </head>
            <body>
                <h1>Learn everything in the world!</h1>
            </body>
        </html>
    """

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(file.router)
app.include_router(comment.router)
app.include_router(like.router)