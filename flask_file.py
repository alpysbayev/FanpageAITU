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


@flask_app.route('/profile/<string:username>')
def profile(username):
    return render_template('profile.html', username=username)


@flask_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        session['authenticated'] = True
        return redirect(url_for('profile', username=username))
    else:
        return render_template('login.html')


@flask_app.route('/signup',  methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password = request.form['password']
        confirm = request.form['confirm']

        return redirect('/login')
    else:
        return render_template('signup.html')
