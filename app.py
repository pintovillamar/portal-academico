from db.database import create_app
from flask_cors import CORS

from models.carreras import carrera_blueprint

app = create_app()

app.register_blueprint(carrera_blueprint)

cors = CORS(app, supports_credentials=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)