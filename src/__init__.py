from flask import Flask
from os import environ
from src.endpoints.users import users
from src.endpoints.incomes import incomes
from src.endpoints.outgoings import outgoings
from src.endpoints.auth import auth
from src.database import db,ma,migrate,jwt

def create_app():
    app = Flask(__name__,
    instance_relative_config=True)

    app.config['ENVIRONMENT'] = environ.get("ENVIRONMENT")
    config_class = 'config.DevelopmentConfig'

    match app.config['ENVIRONMENT']:
        case "development":
            config_class = 'config.DevelopmentConfig'
        case "production":
            config_class = 'config.ProductionConfig'
        case _:
            print(f"ERROR: environment unknown: {app.config.get('ENVIRONMENT')},fallback to {mode}")
    app.config['ENVIRONMENT'] = "development"
    
    app.config.from_object(config_class)
    ##Load the blueprints
    app.register_blueprint(users)
    app.register_blueprint(incomes)
    app.register_blueprint(outgoings)
    app.register_blueprint(auth)
    
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    #Creacion de tablas
    with app.app_context():
        #db.drop_all()
        db.create_all()
        
    return app