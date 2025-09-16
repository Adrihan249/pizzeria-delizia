# 🍕 Pizzería Delizia - Sistema Web de Pedidos

Este proyecto es un sistema web desarrollado con **Python (Flask)** que permite a una pizzería gestionar su catálogo de productos, recibir pedidos online y administrar órdenes desde una interfaz amigable y moderna.

## 🚀 Características Principales

- Registro e inicio de sesión de usuarios (cliente y administrador)
- Catálogo de pizzas y combos con imágenes y descripciones
- Carrito de compras y selección de cantidades
- Proceso de pago con generación de boleta (PDF)
- Panel de administrador para gestionar pedidos en tiempo real
- Diseño responsive con Bootstrap 5

## 🧱 Estructura del Proyecto

```
/pizzeria_project/
│
├── /app/
│   ├── __init__.py
│   ├── admin.py
│   ├── auth.py
│   ├── cliente.py
│   ├── extensions.py
│   ├── models.py
│   ├── main.py
│   └── /templates/
│       ├── /admin/
│       │   └── dashboard.html
│       ├── /cliente/
│       │   ├── carrito.html
│       │   ├── catalogo.html
│       │   ├── home.html
│       │   └── pago.html
│       └── login.html
│
├── /instance/
│   └── pizzeria.db
├── /migrations/
├── modelo.er
├── modelo.png
├── check.py
├── run.py
├── seed.py
├── requirements.txt
└── README.md
```

## 🛠 Tecnologías Utilizadas

- **Lenguaje:** Python 3.11
- **Framework:** Flask
- **ORM:** SQLAlchemy
- **Base de Datos:** SQLite
- **Frontend:** HTML, Bootstrap 5, Font Awesome
- **Templating:** Jinja2
- **Autenticación:** Flask-Login
- **PDF:** ReportLab
- **Testing y desarrollo:** Postman, Flask Debug
- **Deploy sugerido:** Render

## 🧪 Cómo Ejecutar el Proyecto

1. Clona el repositorio:
```bash
git clone https://github.com/Adrihan249/pizzeria-delizia.git
cd pizzeria-delizia
```

2. Crea un entorno virtual:
```bash
python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Inicializa la base de datos:
```bash
flask db init
flask db migrate -m "initial"
flask db upgrade
```

5. Inserta datos de prueba (opcional):
```bash
python seed.py
```

6. Ejecuta la aplicación:
```bash
python run.py
```

7. Accede a la app en tu navegador:
```
http://localhost:5000
```
## 🔀 Flujo de Trabajo con Git

Para mantener un desarrollo organizado, se aplicó un flujo de trabajo basado en ramas y commits atómicos.

### 📂 Ramas
- **main** → rama principal y estable.  
- **feature/nombre** → nuevas funcionalidades.  
- **fix/nombre** → correcciones de errores.  

### 📝 Estilo de Commits
Mensajes claros y descriptivos.  
Ejemplos:  
- `feature: agregar vista de catálogo de productos`  
- `fix: corregir validación en el login`  

### ⚡ Uso de comandos Git
Se documenta el uso de comandos clave:  
- `git switch -c feature/catalogo` → crear rama para el catálogo.  
- `git restore app/templates/cliente/home.html` → restaurar un archivo modificado por error.  
- `git reset --hard HEAD~1` → deshacer el último commit.  
- `git checkout main` → volver a la rama principal.  
- `git merge feature/catalogo` → fusión de la nueva funcionalidad.  

### 🔁 Pull Requests y Conflictos
- Cada cambio mayor se fusiona a **main** mediante **Pull Request**.  
- Se resolvió un conflicto en `models.py` durante la fusión de ramas, manteniendo la versión más actualizada.  
## 🖼️ Capturas de Pantalla
---
### 🏠 Página Principal
---
![Página principal](./screenshots/home.png)
---
### 🛍️ Lista de Productos
---
![Lista productos](./screenshots/lista.png)
---
### 📘 Zona Administrativa
---
![Zona Administrativa](./screenshots/zona.png)
---
## 👤 Roles

- **Cliente:** Puede ver el catálogo, seleccionar productos, enviar pedidos.
- **Administrador:** Puede ver todos los pedidos en tiempo real y gestionar el estado.
