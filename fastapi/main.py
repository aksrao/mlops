from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    firstName: str
    lastName: str
    age: int
    married: bool

@app.get("/")
def root():
    return {"message": "Hello akshay"}

@app.get("/posts")
def get_post():
    return {"data": "your data"}

@app.post("/create")
def create_post(data: Post):
    print(data)
    return {f"First Name" : f"{data.firstName}" , 
            f"Last Name" : f"{data.lastName}", 
            f"Age" : f"{data.age}", 
            f"Is Married" : f"{data.married}"
        }