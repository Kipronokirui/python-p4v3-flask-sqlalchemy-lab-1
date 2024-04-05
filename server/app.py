# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
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

# Add views here
@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    earthquake = Earthquake.query.filter_by(id=id).first()

    if earthquake:
        response_body = earthquake.to_dict()
        response_status = 200
    else:
        response_body = {
            'message':f'Earthquake {id} not found.'
        }
        response_status = 404
    
    response = make_response(response_body, response_status)
    return response

@app.route('/earthquakes/magnitude/<float:magnitude>')
def filter_by_magnitude(magnitude):
    filtered_earthquakes = []
    earthquakes=Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    for earthquake in earthquakes:
        filtered_earthquakes.append(earthquake.to_dict())
    response_body = {
        'count':len(filtered_earthquakes),
        'quakes':filtered_earthquakes
    }
    response = make_response(response_body, 200)
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
