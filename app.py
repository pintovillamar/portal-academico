from db.database import create_app
from flask_cors import CORS

from models.carreras import carrera_blueprint
from models.usuarios import usuario_blueprint
from models.estudiantes import estudiante_blueprint
from models.test import test_blueprint

app = create_app()

app.register_blueprint(carrera_blueprint)
app.register_blueprint(usuario_blueprint)
app.register_blueprint(estudiante_blueprint)
app.register_blueprint(test_blueprint)

@app.route('/')
def index():
    return "Hello, World!"

cors = CORS(app, supports_credentials=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)