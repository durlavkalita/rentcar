from app.main import bp
from flask import send_file, render_template

@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@bp.route('/swagger-ui')
def serve_swagger_ui():
    return send_file('swagger.yaml', mimetype='text/yaml')
