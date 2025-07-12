from app import create_app, db
from app.models import Producto

app = create_app()
app.app_context().push()

# Datos de ejemplo
productos = [
    Producto(nombre="Pizza Margarita", descripcion="Queso, tomate y albahaca", precio=25.0, tipo="pizza"),
    Producto(nombre="Pizza Pepperoni", descripcion="Queso mozzarella y pepperoni", precio=28.0, tipo="pizza"),
    Producto(nombre="Pizza Hawaiana", descripcion="Jamón y piña", precio=27.0, tipo="pizza"),
    Producto(nombre="Combo Familiar", descripcion="2 Pizzas grandes + gaseosa", precio=60.0, tipo="combo"),
    Producto(nombre="Combo Individual", descripcion="1 Pizza personal + gaseosa", precio=35.0, tipo="combo"),
    Producto(nombre="Pizza Vegetariana", descripcion="Pimientos, champiñones, cebolla", precio=26.0, tipo="pizza"),
]

# Insertar productos solo si no existen
for producto in productos:
    existe = Producto.query.filter_by(nombre=producto.nombre).first()
    if not existe:
        db.session.add(producto)

db.session.commit()

print("✅ Productos añadidos con éxito (sin duplicados).")
