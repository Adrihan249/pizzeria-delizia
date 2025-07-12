from flask import Blueprint, redirect, url_for
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    if current_user.rol == 'admin':
        return redirect(url_for('admin.dashboard'))
    elif current_user.rol == 'cliente':
        return redirect(url_for('cliente.home'))
    else:
        return redirect(url_for('auth.login'))
