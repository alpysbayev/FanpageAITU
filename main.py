from flask_file import flask_app
from fastapi_file import fastapi_app
from fastapi.middleware.wsgi import WSGIMiddleware
import uvicorn

fastapi_app.mount('/', WSGIMiddleware(flask_app))

if __name__ == "__main__":
    uvicorn.run("main:fastapi_app", host='127.0.0.1', port=2003, reload=True, debug=True)
