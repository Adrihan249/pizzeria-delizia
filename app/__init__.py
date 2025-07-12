from flask import Flask
from .extensions import db, login_manager
from .models import Usuario
from flask_migrate import Migrate 
from datetime import timedelta
migrate = Migrate()
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'clave-secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizzeria.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['REMEMBER_COOKIE_DURATION'] = 0

    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=3)




    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    with app.app_context():
        from . import models
        db.create_all()

        # Crear admin automáticamente si no existe
        if not Usuario.query.filter_by(username='admin1').first():
            admin = Usuario(username='admin1', rol='admin')
            admin.set_password('admin1')
            db.session.add(admin)
            db.session.commit()
            print('Administrador creado automáticamente.')

    from .main import main as main_blueprint
    from .auth import auth
    from .admin import admin
    from .cliente import cliente 
    
    app.register_blueprint(main_blueprint)

    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(cliente)

    return app
