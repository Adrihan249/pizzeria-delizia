from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db


class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    rol = db.Column(db.String(10))  # 'admin' o 'cliente'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.String(500), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    imagen = db.Column(db.String(500))  # ✅ Aquí agregamos el campo imagen (como URL)

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_cliente = db.Column(db.String(100))
    direccion = db.Column(db.String(200), nullable=True)
    total = db.Column(db.Float, default=0)
    estado = db.Column(db.String(20), default='En proceso')
    fecha = db.Column(db.DateTime, server_default=db.func.now())
    detalles = db.relationship('PedidoDetalle', backref='pedido', cascade="all, delete-orphan")

class PedidoDetalle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'))
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'))
    cantidad = db.Column(db.Integer)
    subtotal = db.Column(db.Float)

    producto = db.relationship('Producto')
