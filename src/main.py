import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import authrouter
from routes.users import usersrouter

from config.database import create_table


app = FastAPI()


@app.on_event("startup")
async def runtimestartup():
    create_table()


# asa

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def hello():
    return "Hello"


## Test


app.include_router(authrouter.router)
app.include_router(usersrouter.router)


# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True)
