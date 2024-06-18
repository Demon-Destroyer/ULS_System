from flask import Flask
from flask_cors import CORS
from config import Localconfig

def create_app(config_class=Localconfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.app_context().push()
    
    # Initialize Flask extensions here
    from uls_app.extensions import db, api
    db.init_app(app)
    CORS(
        app,
        origins="http://localhost:8081",
    )
    
    # Register blueprints here
    from uls_app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from uls_app.resources.userResource import UserResource
    
    api.add_resource(UserResource, "/users", "/user/<int:user_id>")
    
    api.init_app(app)
    
    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'
    
    @app.route('/api/v1/status')
    def index():
        return {"status" : "ok"}

    return app