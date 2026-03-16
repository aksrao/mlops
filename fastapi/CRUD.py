from random import randrange
from fastapi import FastAPI ,status, HTTPException, Response
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    firstName: str
    age: int
try:
    conn = psycopg2.connect(host='localhost',database='akshayrao', user='postgres', port='5435', password='password123', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database conection as secussfull")
except Exception as error:
    print("connecting to db failed")
    print("Errror", error)


my_post = [{"id": 1,"firstName": "akshay", "age": 28 }, {"id": 2,"firstName": "geeta", "age": 54}]

def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_post):
        if p["id"] == id:
            return i

@app.get("/")
def root():
    return {"message": "Hello akshay"}

@app.get("/posts")
def get_posts():
    return {"data": my_post }

@app.post("/create")
def create_post(data: Post):
    data_dict = data.model_dump()
    data_dict['id'] = randrange(0,100)
    my_post.append(data_dict)
    return {"data": data_dict}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    return post
    
@app.delete("/posts/{id}")
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"data not found")
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)