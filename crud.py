from sqlalchemy.orm import Session
import schemas
import models
import hashlib


def hash_password(password):
    hash_pass = hashlib.md5(password.encode())
    return hash_pass.hexdigest()


def get_occupancy_username(db: Session, user_id: int, new_username: str):
    query = db.query(models.User.username).filter(models.User.id != user_id).all()

    other_usernames = []
    for i in range(len(query)):
        other_usernames += query[i]

    if new_username in other_usernames:
        return True
    else:
        return False


def get_hashed_password(db: Session, user_id: int):
    result = (db.query(models.User.hashed_password).filter(models.User.id == user_id).first())[0]
    return result


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_post_by_id(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def get_user_posts(db: Session, user_id: int):
    return db.query(models.Post).filter(models.Post.author_id == user_id).all()


def get_all_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()


def delete_post(db: Session, post_id: int):
    db.query(models.Post).filter(models.Post.id == post_id).delete()

    db.commit()

    return None


def delete_user(db: Session, user_id: int):
    db.query(models.User).filter(models.User.id == user_id).delete()

    db.commit()

    return None


def clear_posts(db: Session, user_id: int):
    db.query(models.Post).filter(models.Post.author_id == user_id).delete()

    db.commit()

    return None


def change_password(db: Session, user_id: int, new_password: str):
    user = get_user_by_id(db=db, user_id=user_id)
    user.hashed_password = hash_password(new_password)

    db.commit()
    db.refresh(user)

    return user


def update_post(db: Session, post_id: int, updated_post: schemas.PostCreate):
    post = get_post_by_id(db=db, post_id=post_id)
    post.title = updated_post.title
    post.description = updated_post.description
    post.text = updated_post.text

    db.commit()
    db.refresh(post)

    return post


def update_user(db: Session, user_id: int, updated_user: schemas.UserCreate):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    user.username = updated_user.username
    user.firstname = updated_user.firstname
    user.lastname = updated_user.lastname
    user.hashed_password = hash_password(updated_user.password)

    db.commit()
    db.refresh(user)

    return user


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_password,
                           firstname=user.firstname, lastname=user.lastname)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def create_user_post(db: Session, post: schemas.PostCreate, user_id: int):
    new_post = models.Post(**post.dict(), author_id=user_id)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
