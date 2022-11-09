from flask import Flask, render_template, request, flash, redirect, session, url_for
from fastapi_file import db
import crud
import schemas

flask_app = Flask(__name__)
flask_app.config['SECRET_KEY'] = 'super_secret'


@flask_app.route('/')
def home():
    return render_template('index.html')


@flask_app.route('/about')
def about():
    return render_template('about.html')


@flask_app.route('/contact')
def contact():
    return render_template('contact.html')


@flask_app.route('/posts')
def posts():
    all_posts = crud.get_all_posts(db)
    return render_template('posts.html', all_posts=all_posts)


@flask_app.route('/posts/<int:post_id>/detail', methods=['GET', 'POST'])
def post_detail(post_id):
    if request.method == 'POST':
        comment = schemas.CommentCreate(text=request.form['comment'])

        crud.create_comment(db=db, comment=comment, user_id=session['user_id'], post_id=post_id)

        return redirect(request.url)
    else:
        likes = crud.get_post_likes(db=db, post_id=post_id)
        comments = crud.get_post_comments(db=db, post_id=post_id)
        post = crud.get_post_by_id(db=db, post_id=post_id)
        return render_template('post_detail.html', post=post, comments=comments, likes=likes)


@flask_app.route('/posts/<int:post_id>/detail/comments/<int:comment_id>/delete', methods=['POST', 'GET'])
def delete_comment(comment_id, post_id):
    crud.delete_comment(db=db, comment_id=comment_id)
    return redirect(url_for('post_detail', post_id=post_id))


@flask_app.route('/posts/<int:post_id>/detail/like/user/<int:user_id>', methods=['GET'])
def like(post_id, user_id):
    check_like = crud.check_like(db=db, user_id=user_id, post_id=post_id)

    if check_like:
        crud.delete_like(db=db, user_id=user_id, post_id=post_id)
        return redirect(url_for('post_detail', post_id=post_id))
    else:
        crud.create_like(db=db, user_id=user_id, post_id=post_id)
        return redirect(url_for('post_detail', post_id=post_id))


@flask_app.route('/users/<int:user_id>/create_post', methods=['GET', 'POST'])
def create_post(user_id):
    if request.method == 'POST':
        post = schemas.PostCreate(title=request.form['title'], description=request.form['description'],
                                  text=request.form['text'])

        crud.create_user_post(db=db, post=post, user_id=user_id)

        return redirect(url_for('posts'))
    else:
        return render_template('create_post.html')


@flask_app.route('/profile/<int:user_id>')
def profile(user_id):
    user = crud.get_user_by_id(db=db, user_id=user_id)
    return render_template('profile.html', user=user)


@flask_app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_data = schemas.UserCreate(username=request.form["username"], firstname=request.form["firstname"],
                                       lastname=request.form["lastname"], password=request.form["password"])

        existence_user = crud.get_user_by_username(db=db, username=user_data.username)

        if existence_user:
            flash('Username is already in use!')
            return redirect(request.url)

        elif request.form["password"] != request.form['confirm']:
            flash("Password doesn't match!")
            return redirect(request.url)

        else:
            crud.create_user(db=db, user=user_data)
            return redirect('/login')
    else:
        return render_template('signup.html')


@flask_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = crud.get_user_by_username(db=db, username=username)

        if not user:
            flash("There's no such user!")
            return redirect(request.url)
        elif crud.hash_password(password) != user.hashed_password:
            flash('Wrong password!')
            return redirect(request.url)
        else:
            session['authenticated'] = True
            session['user_id'] = user.id
            return redirect(url_for('profile', user_id=user.id))
    else:
        return render_template('login.html')


@flask_app.route('/logout')
def logout():
    session.pop('authenticated', None)
    session.pop('user_id', None)
    return redirect(url_for('home'))
