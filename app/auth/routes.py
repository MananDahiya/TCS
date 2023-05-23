from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models.user import User
from app.auth import bp

@bp.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email = email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Incorrect credentials, Please try again.')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember = remember)
        return redirect(url_for('main.profile'))
    
    return render_template('auth/login.html')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('first-name')
        lastname = request.form.get('last-name')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()

        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))
        
        new_user = User(email = email, firstname = firstname, lastname = lastname, password = generate_password_hash(password, method = 'sha256'))
        db.session.add(new_user)
        db.session.commit()

        flash('User successfully created')

        return redirect(url_for('auth.login'))
    
    return render_template('auth/signup.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
