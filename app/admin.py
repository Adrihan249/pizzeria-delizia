from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from .models import Usuario, Producto, Pedido
from . import db

admin = Blueprint('admin', __name__, url_prefix='/admin')

def solo_admin(f):
    from functools import wraps
    @wraps(f)
    def decorador(*args, **kwargs):
        if not current_user.is_authenticated or current_user.rol != 'admin':
            flash("Acceso denegado")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorador

@admin.route('/dashboard', methods=['GET', 'POST'])
@login_required
@solo_admin
def dashboard():
    if request.method == 'POST':
        # Crear usuario
        if 'crear_usuario' in request.form:
            username = request.form['username']
            password = request.form['password']
            rol = request.form['rol']
            if Usuario.query.filter_by(username=username).first():
                flash('El usuario ya existe.')
            else:
                nuevo_usuario = Usuario(username=username, rol=rol)
                nuevo_usuario.set_password(password)
                db.session.add(nuevo_usuario)
                db.session.commit()
                flash('Usuario creado exitosamente.')

        # Eliminar usuario
        if 'eliminar_usuario' in request.form:
            usuario_id = request.form['eliminar_usuario']
            usuario = Usuario.query.get(usuario_id)
            if usuario:
                db.session.delete(usuario)
                db.session.commit()
                flash('Usuario eliminado.')

        # Crear producto
        if 'crear_producto' in request.form:
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            precio = request.form['precio']
            tipo = request.form['tipo']
            imagen = request.form['imagen']
            nuevo_producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio, tipo=tipo, imagen=imagen)
            db.session.add(nuevo_producto)
            db.session.commit()
            flash('Producto creado exitosamente.')

        # Eliminar producto
        if 'eliminar_producto' in request.form:
            producto_id = request.form['eliminar_producto']
            producto = Producto.query.get(producto_id)
            if producto:
                db.session.delete(producto)
                db.session.commit()
                flash('Producto eliminado.')

        # Editar producto
        if 'editar_producto' in request.form:
            producto_id = request.form['editar_producto']
            producto = Producto.query.get(producto_id)
            if producto:
                producto.nombre = request.form[f'nombre_{producto_id}']
                producto.descripcion = request.form[f'descripcion_{producto_id}']
                producto.precio = request.form[f'precio_{producto_id}']
                producto.tipo = request.form[f'tipo_{producto_id}']
                producto.imagen = request.form[f'imagen_{producto_id}']
                db.session.commit()
                flash('Producto actualizado.')

        # Cambiar estado del pedido
        if 'cambiar_estado' in request.form:
            pedido_id = request.form['pedido_id']
            nuevo_estado = request.form['cambiar_estado']

            pedido = Pedido.query.get(pedido_id)
            if pedido:
                pedido.estado = nuevo_estado
                db.session.commit()
                flash(f'El pedido {pedido.id} cambió a {nuevo_estado}.')

        return redirect(url_for('admin.dashboard'))

    usuarios = Usuario.query.all()
    productos = Producto.query.all()
    pedidos = Pedido.query.all()

    return render_template('admin/dashboard.html', usuarios=usuarios, productos=productos, pedidos=pedidos)
