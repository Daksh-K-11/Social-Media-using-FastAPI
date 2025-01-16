from .. import models, schemas, utils, oauth2
from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_post(db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user), 
             limit = 10, skip: int = 0, search: Optional[str] = ""):
    # cur.execute("""SELECT * FROM posts""")
    # posts = cur.fetchall()
    # print(search)
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Post.id==models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db : Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    
    # cur.execute("""INSERT INTO posts (title, content, published) values (%s,%s,%s) RETURNING *""",
    #             (post.title, post.content, post.published))
    # post = cur.fetchone()
    # con.commit()
    
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id : int, response: Response, db : Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    
    # cur.execute("""SELECT * FROM posts WHERE id=%s""",(str(id),))
    # post = cur.fetchone()
    
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.id==id).first()
    
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} was not found')
    
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    
    # cur.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",((str(id)),))
    # deleted_post = cur.fetchone()
    # con.commit()
    # print(deleted_post)
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform requested action')
    
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db : Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    
    # cur.execute("""UPDATE posts SET title=%s, content=%s, published=%s where id=%s RETURNING *"""
    #             ,(post.title, post.content, post.published, id))
    # updated_post = cur.fetchone()
    # con.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform requested action')
        
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()
