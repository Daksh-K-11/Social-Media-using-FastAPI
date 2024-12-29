from .. import models, schemas, utils
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
    prefix="/user",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db : Session =  Depends(get_db)):
    
    user.password = utils.hash(user.password)
    
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db : Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == id).first()
    print(user)
    print(db.query(models.User).filter(models.User.id == id))
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'User with id {id} does not exist')
    return user
    