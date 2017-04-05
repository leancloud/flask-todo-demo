# coding: utf-8

from leancloud import User
from leancloud import LeanCloudError
from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask import flash


users_view = Blueprint('users', __name__)


@users_view.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('users/register.html')
    if request.method == 'POST':
        user = User()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if not username or not password:
            flash('用户名和密码不能为空。')
            return redirect(url_for('users.register'))
        user.set_username(username)
        user.set_password(password)
        try:
            user.sign_up()
        except LeanCloudError as e:
            flash(e.error)
            return redirect(url_for('users.register'))
        return redirect(url_for('todos.show'))


@users_view.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('users/login.html')
    if request.method == 'POST':
        user = User()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if not username or not password:
            flash('用户名和密码不能为空。')
            return redirect(url_for('users.login'))
        try:
            user.login(username, password)
        except LeanCloudError as e:
            flash(e.error)
            return redirect(url_for('users.login'))
        return redirect(url_for('todos.show'))


@users_view.route('/logout')
def logout():
    current_user = User.get_current()
    if current_user:
        current_user.logout()
        flash('你已登出。')
    return redirect(url_for('users.login'))
