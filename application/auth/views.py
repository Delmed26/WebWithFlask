from multiprocessing import context
from flask import render_template, session, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash
from application.forms import LoginForm
from . import auth
from application.firestore_service import get_user, user_put
from application.models import UserData, UserModel

@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict()['password']

            if password_from_db != password:
                flash('Wrong password')
            else:
                user_data = UserData(username, password)
                user = UserModel(user_data)

                login_user(user)
                flash('Logged in successfully')

                redirect(url_for('hello'))
        else:
            flash('User not found')

        return redirect(url_for('hello'))

    return render_template('login.html', **context)


@auth.route('signup', methods=['GET', 'POST'])
def signup():
    signup_form = LoginForm()
    context = {
        'signup_form' : signup_form
    }
    
    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is None:
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password_hash)
            user_put(user_data)

            user = UserModel(user_data=user_data)

            login_user(user)

            flash('User created successfully')

            return redirect(url_for('hello'))

        else:
            flash('User already exists')


    return render_template('signup.html', **context)

@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully')
    return redirect(url_for('auth.login'))