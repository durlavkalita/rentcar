from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from redis import Redis

redis_client = Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    SWAGGER_URL = app.config.get("SWAGGER_URL", "/api/docs") 
    API_URL = app.config.get("API_URL", "/static/swagger.json")

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.business import bp as business_bp
    app.register_blueprint(business_bp, url_prefix="/business")

    from app.car import bp as cars_bp
    app.register_blueprint(cars_bp, url_prefix="/cars")
    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Car rent application"
        },
        # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
        #    'clientId': "your-client-id",
        #    'clientSecret': "your-client-secret-if-required",
        #    'realm': "your-realms",
        #    'appName': "your-app-name",
        #    'scopeSeparator': " ",
        #    'additionalQueryStringParams': {'test': "hello"}
        # }
    )

    app.register_blueprint(swaggerui_blueprint)
    
    return app

from app import models
