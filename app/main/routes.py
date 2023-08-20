from app.main import bp
from flask import send_file

@bp.route('/', methods=['GET'])
def index():
    return {"message": "hello world"}

@bp.route('/swagger-ui')
def serve_swagger_ui():
    return send_file('swagger.yaml', mimetype='text/yaml')
