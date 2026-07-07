from flask import Blueprint, render_template, request, redirect, url_for, session
from config import Config

auth_bp = Blueprint('auth', __name__)

def is_admin():
    return session.get('admin_logged_in')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == Config.ADMIN_USER and request.form['password'] == Config.ADMIN_PASS:
            session['admin_logged_in'] = True
            return redirect(url_for('dashboard.index'))
        return render_template('login.html', error="Sai tài khoản hoặc mật khẩu")
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
    