from flask import Flask, render_template, request, flash, redirect, session, url_for
# from fastapi_file import db
# import crud
# import schemas

flask_app = Flask(__name__)
flask_app.config['SECRET_KEY'] = 'super_secret'


@flask_app.route('/')
def home():
    return render_template('index.html')


@flask_app.route('/about')
def about():
    return render_template('about.html')


@flask_app.route('/posts')
def posts():
    return render_template('posts.html')


@flask_app.route('/contact')
def contact():
    return render_template('contact.html')


@flask_app.route('/login')
def login():
    return render_template('login.html')


@flask_app.route('/signup')
def signup():
    return render_template('signup.html')
