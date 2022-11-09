from fastapi import FastAPI, Depends
# from database import *
# import models
# import crud
# import schemas

# models.Base.metadata.create_all(bind=engine)


# def get_db():
#     db_conn = SessionLocal()
#     try:
#         yield db_conn
#     finally:
#         db_conn.close()
#
#
# db = next(Depends(get_db).dependency())

fastapi_app = FastAPI()
