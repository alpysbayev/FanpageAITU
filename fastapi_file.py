from fastapi import FastAPI, Depends
from database import *
import models
import crud
import schemas

models.Base.metadata.create_all(bind=engine)


def get_db():
    db_conn = SessionLocal()
    try:
        yield db_conn
    finally:
        db_conn.close()


db = next(Depends(get_db).dependency())

fastapi_app = FastAPI()


@fastapi_app.post('/create/user')
def create_user(user: schemas.UserCreate):
    return crud.create_user(db=db, user=user)


@fastapi_app.post('/create/post')
def create_post(post: schemas.PostCreate, user_id: int):
    return crud.create_user_post(db=db, post=post, user_id=user_id)


@fastapi_app.get('/read/users')
def read_users():
    return crud.get_all_users(db=db)


@fastapi_app.get('/read/posts')
def read_posts():
    return crud.get_all_posts(db=db)


@fastapi_app.get('/read/user/posts')
def read_user_posts(user_id: int):
    return crud.get_user_posts(db=db, user_id=user_id)


@fastapi_app.put('/update/post')
def update_post(updated_post: schemas.PostCreate, post_id: int):
    return crud.update_post(db=db, updated_post=updated_post, post_id=post_id)


@fastapi_app.put('/update/user')
def update_user(updated_user: schemas.UserCreate, user_id: int):
    return crud.update_user(db=db, updated_user=updated_user, user_id=user_id)


@fastapi_app.put('/update/user/change_password')
def change_password(user_id: int, new_password: str):
    return crud.change_password(db=db, user_id=user_id, new_password=new_password)


@fastapi_app.delete('/delete/post')
def delete_post(post_id: int):
    return crud.delete_post(db=db, post_id=post_id)


@fastapi_app.delete('/delete/user')
def delete_user(user_id: int):
    return crud.delete_user(db=db, user_id=user_id)


@fastapi_app.delete('/clear/user/posts')
def clear_user_posts(user_id: int):
    return crud.clear_posts(db=db, user_id=user_id)
