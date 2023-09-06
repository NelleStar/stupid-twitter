from flask import Flask, render_template, redirect, session, flash
from models import connect_db, db, User, Tweet
from forms import UserForm

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///auth_demo"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["SECRET_KEY"] = "abc123"

app.app_context().push()
connect_db(app)


@app.route('/')
def home_page():
    """renders home page"""
    return render_template('index.html')

@app.route('/tweets')
def show_tweets():
    if "user_id" not in session:
        flash('Please login or register first!')
        return redirect('/login')
    return render_template("tweets.html")

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        new_user = User.register(username, password)

        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id

        flash("Welcome! You have successfully created an account!")
        return redirect('/tweets')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome back, {user.username}!")
            session['user_id'] = user.id

            return redirect('/tweets')
        else:
            form.username.errors = ['Invalid username/password']

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    session.pop('user_id')
    return redirect('/')


