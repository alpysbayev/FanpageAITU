from pydantic import BaseModel


class LikeBase(BaseModel):
    pass


class LikeCreate(LikeBase):
    pass


class Like(LikeBase):
    id: int

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    text: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    author_id: int
    post_id: int

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    description: str
    text: str


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    firstname: str
    lastname: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    posts: list[Post] = []

    class Config:
        orm_mode = True
