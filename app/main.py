from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import models, schemas, utils
from typing import List
from .routers import post, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:    
    try:
        con = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                            password='Chennai@05', cursor_factory=RealDictCursor)
        cur = con.cursor()
        print('DB connection established')
        break
    except Exception as e:
        print("Unable to connect to the database")
        print("Error: ",e)
        time.sleep(2)
        
my_posts = [
        {"title": "title of post 1", "content": "content of post 1", "id": 1}, 
        {"title":"favourite foods", "content": "I like pizza", "id": 2},
            ]

def find_post_index(id : int):
    for i in range(len(my_posts)):
        if my_posts[i]['id']==id:
            return i
    return None



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hey daksh its me"}


