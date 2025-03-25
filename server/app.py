from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Updated query method
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    try:
        earthquake = db.session.get(Earthquake, id)  # Use SQLAlchemy 2.0 method
        if earthquake:
            return jsonify({
                "id": earthquake.id,
                "location": earthquake.location,
                "magnitude": earthquake.magnitude,
                "year": earthquake.year
            }), 200
        else:
            return jsonify({"message": f"Earthquake {id} not found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Better error handling


@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    try:
        quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
        quake_list = [
            {
                "id": q.id,
                "location": q.location,
                "magnitude": q.magnitude,
                "year": q.year
            }
            for q in quakes
        ]

        return jsonify({"count": len(quake_list), "quakes": quake_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Error handling


if __name__ == '__main__':
    app.run(port=5555, debug=True)
