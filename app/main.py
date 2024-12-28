from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import models
from . import schemas
from typing import List

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

@app.get("/")
def root():
    return {"message": "Hey daksh its me"}



@app.get("/posts", response_model=List[schemas.Post])
def get_post(db: Session = Depends(get_db)):
    # cur.execute("""SELECT * FROM posts""")
    # posts = cur.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db : Session = Depends(get_db)):
    
    # cur.execute("""INSERT INTO posts (title, content, published) values (%s,%s,%s) RETURNING *""",
    #             (post.title, post.content, post.published))
    # post = cur.fetchone()
    # con.commit()
    
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@app.get("/posts/{id}",response_model=schemas.Post)
def get_post(id : int, response: Response, db : Session = Depends(get_db)):
    
    # cur.execute("""SELECT * FROM posts WHERE id=%s""",(str(id),))
    # post = cur.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} was not found')
    
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db)):
    
    # cur.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",((str(id)),))
    # deleted_post = cur.fetchone()
    # con.commit()
    # print(deleted_post)
    
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}",response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db : Session = Depends(get_db)):
    
    # cur.execute("""UPDATE posts SET title=%s, content=%s, published=%s where id=%s RETURNING *"""
    #             ,(post.title, post.content, post.published, id))
    # updated_post = cur.fetchone()
    # con.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
        
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()
    
@app.post("/user", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db : Session =  Depends(get_db)):
    
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user