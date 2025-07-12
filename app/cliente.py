from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from .models import Producto, Pedido
from . import db
from .models import Producto, Pedido, PedidoDetalle
from flask import send_file
from reportlab.pdfgen import canvas
import io
from reportlab.lib.pagesizes import letter


cliente = Blueprint('cliente', __name__, url_prefix='/cliente')

@cliente.route('/home')
@login_required
def home():
    return render_template('cliente/home.html')
@cliente.route('/catalog', methods=['GET', 'POST'])
@login_required
def catalog():
    pizzas = Producto.query.filter_by(tipo='pizza').all()
    combos = Producto.query.filter_by(tipo='combo').all()

    if request.method == 'POST':
        carrito = {}
        for producto in pizzas + combos:
            cantidad = int(request.form.get(f'cantidad_{producto.id}', 0))
            if cantidad > 0:
                carrito[str(producto.id)] = cantidad

        if not carrito:
            flash('Debes seleccionar al menos un producto o combo con cantidad mayor a 0.')
            return redirect(url_for('cliente.catalog'))

        session['carrito'] = carrito

        # ✅ Crear pedido inmediatamente con estado "en proceso"
        nuevo_pedido = Pedido(
            nombre_cliente=current_user.username,
            direccion='',  # Se completará luego
            estado='en proceso'
        )
        db.session.add(nuevo_pedido)
        db.session.commit()
        session['pedido_id'] = nuevo_pedido.id

        # ✅ Crear los detalles del pedido
        for producto_id, cantidad in carrito.items():
            detalle = PedidoDetalle(
                pedido_id=nuevo_pedido.id,
                producto_id=int(producto_id),
                cantidad=cantidad
            )
            db.session.add(detalle)

        db.session.commit()

        return redirect(url_for('cliente.carrito'))

    return render_template('cliente/catalogo.html', pizzas=pizzas, combos=combos)


@cliente.route('/carrito', methods=['GET', 'POST'])
@login_required
def carrito():
    carrito = session.get('carrito', {})
    productos = []
    total = 0

    for producto_id, cantidad in carrito.items():
        producto = Producto.query.get(int(producto_id))
        subtotal = producto.precio * cantidad
        productos.append({'producto': producto, 'cantidad': cantidad, 'subtotal': subtotal})
        total += subtotal

    # Crear pedido solo si no existe aún
    if 'pedido_id' not in session and productos:
        nuevo_pedido = Pedido(
            nombre_cliente=current_user.username,
            direccion='',
            total=0,
            estado='en proceso'
        )
        db.session.add(nuevo_pedido)
        db.session.commit()

        session['pedido_id'] = nuevo_pedido.id

        for item in productos:
            detalle = PedidoDetalle(
                pedido_id=nuevo_pedido.id,
                producto_id=item['producto'].id,
                cantidad=item['cantidad']
            )
            db.session.add(detalle)
        db.session.commit()

    pedido_id = session.get('pedido_id')

    if request.method == 'POST':
        accion = request.form.get('accion')
        pedido = Pedido.query.get(pedido_id)

        if accion == 'cancelar':
            pedido.estado = 'cancelado'
            pedido.total = 0
            db.session.commit()
            flash('Pedido cancelado.')
            session.pop('carrito', None)
            session.pop('pedido_id', None)
            return redirect(url_for('cliente.pago'))

        if accion == 'confirmar':
            direccion = request.form['direccion']
            pedido.estado = 'completado'
            pedido.direccion = direccion

            # ✅ Recalcular total desde los detalles guardados
            detalles = PedidoDetalle.query.filter_by(pedido_id=pedido.id).all()
            pedido.total = sum(detalle.producto.precio * detalle.cantidad for detalle in detalles)

            db.session.commit()
            flash('Compra confirmada.')
            session.pop('carrito', None)
            
            return redirect(url_for('cliente.pago'))

    return render_template('cliente/carrito.html', productos=productos, total=total)


@cliente.route('/pago', methods=['GET', 'POST'])
@login_required
def pago():
    pedido_id = session.get('pedido_id')

    if not pedido_id:
        flash('No hay pedido pendiente.')
        return redirect(url_for('cliente.catalog'))

    pedido = Pedido.query.get(pedido_id)
    detalles = PedidoDetalle.query.filter_by(pedido_id=pedido_id).all()

    if request.method == 'POST':
        # Datos adicionales del formulario
        nombre_completo = request.form['nombre_completo']
        fecha_nacimiento = request.form['fecha_nacimiento']
        email = request.form['email']
        direccion = request.form['direccion']
        nombre_tarjeta = request.form['nombre_tarjeta']
        numero_tarjeta = request.form['numero_tarjeta']

        # Actualizamos dirección del pedido (por si no estaba seteada)
        pedido.direccion = direccion
        db.session.commit()

        # Generar PDF con diseño tipo boleta
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setTitle(f"Boleta_Pedido_{pedido.id}")

        width, height = letter

        # Encabezado
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawCentredString(width / 2, height - 50, "Pizzería Delizia")

        pdf.setFont("Helvetica", 12)
        pdf.drawCentredString(width / 2, height - 70, "RUC: 123456789 | Av. Principal 123, Ciudad")
        pdf.drawCentredString(width / 2, height - 85, f"Boleta de Venta Electrónica Nº {pedido.id}")

        y = height - 120

        # Datos del cliente
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y, "Datos del Cliente:")
        pdf.setFont("Helvetica", 11)
        pdf.drawString(60, y - 15, f"Nombre: {nombre_completo}")
        pdf.drawString(60, y - 30, f"DNI/Nacimiento: {fecha_nacimiento}")
        pdf.drawString(60, y - 45, f"Correo: {email}")
        pdf.drawString(60, y - 60, f"Dirección: {direccion}")

        y -= 90

        # Detalles del pedido
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y, "Detalle de Productos")
        y -= 20

        pdf.setFont("Helvetica", 11)
        total = 0
        for detalle in detalles:
            linea = f"- {detalle.producto.nombre} x {detalle.cantidad} = S/ {detalle.producto.precio * detalle.cantidad:.2f}"
            pdf.drawString(60, y, linea)
            total += detalle.producto.precio * detalle.cantidad
            y -= 18

        y -= 10
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(60, y, f"Total Pagado: S/ {total:.2f}")

        y -= 40
        pdf.setFont("Helvetica", 10)
        pdf.drawString(50, y, f"Fecha: {pedido.fecha.strftime('%d/%m/%Y %H:%M:%S')}")
        pdf.drawString(50, y - 15, "Gracias por tu compra. ¡Te esperamos pronto!")

        pdf.save()
        buffer.seek(0)

        # Limpiar sesión
        session.pop('pedido_id', None)
        session.pop('carrito', None)

        return send_file(buffer, as_attachment=True,
                         download_name=f"Boleta_Pedido_{pedido.id}.pdf",
                         mimetype='application/pdf')

    return render_template('cliente/pago.html', pedido=pedido)