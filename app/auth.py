from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from .models import Usuario
from .extensions import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'login' in request.form:
            username = request.form['username']
            password = request.form['password']
            user = Usuario.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user, remember=False)  # 👉 recordar desactivado
                session.permanent = True  # 👉 Esto está bien aquí
                if user.rol == 'admin':
                    return redirect(url_for('admin.dashboard'))
                elif user.rol == 'cliente':
                    return redirect(url_for('cliente.home'))
                else:
                    return redirect(url_for('auth.login'))
            else:
                flash('Credenciales incorrectas')
        elif 'register' in request.form:
            new_username = request.form['new_username']
            new_password = request.form['new_password']
            if Usuario.query.filter_by(username=new_username).first():
                flash('El usuario ya existe')
            else:
                nuevo_usuario = Usuario(username=new_username, rol='cliente')
                nuevo_usuario.set_password(new_password)
                db.session.add(nuevo_usuario)
                db.session.commit()
                flash('Usuario registrado con éxito. Ahora puedes iniciar sesión.')

    # 👉 Este return siempre debe estar al final, para GET o cuando no haya redirección
    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada con éxito')
    return redirect(url_for('auth.login'))
