from .. import models, schemas, utils
from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.Post])
def get_post(db: Session = Depends(get_db)):
    # cur.execute("""SELECT * FROM posts""")
    # posts = cur.fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
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


@router.get("/{id}",response_model=schemas.Post)
def get_post(id : int, response: Response, db : Session = Depends(get_db)):
    
    # cur.execute("""SELECT * FROM posts WHERE id=%s""",(str(id),))
    # post = cur.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} was not found')
    
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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

@router.put("/{id}",response_model=schemas.Post)
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
