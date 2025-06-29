from flask import Flask, make_response, jsonify, request, send_from_directory
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError

from models import db, Episode, Appearance, Guest

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS for all routes
CORS(app)

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)


@app.route('/')
def welcome():
    response = make_response(
        '<h1>Welcome to the Late Show API!</h1>',
        200
    )
    return response

# GET /episodes
@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    episodes_data = [episode.to_dict(only=('id', 'date', 'number')) for episode in episodes]
    return jsonify(episodes_data)

# GET /episodes/:id
@app.route('/episodes/<int:id>', methods=['GET'])
def get_episode_by_id(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404
    
    episode_data = episode.to_dict(only=('id', 'date', 'number', 'appearances'))
    return jsonify(episode_data)

# GET /guests
@app.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    guests_data = [guest.to_dict(only=('id', 'name', 'occupation')) for guest in guests]
    return jsonify(guests_data)

# POST /appearances
@app.route('/appearances', methods=['POST'])
def create_appearance():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'rating' not in data or 'episode_id' not in data or 'guest_id' not in data:
            return jsonify({"errors": ["Missing required fields: rating, episode_id, guest_id"]}), 400
        
        # Check if episode and guest exist
        episode = Episode.query.get(data['episode_id'])
        guest = Guest.query.get(data['guest_id'])
        
        if not episode:
            return jsonify({"errors": ["Episode not found"]}), 400
        
        if not guest:
            return jsonify({"errors": ["Guest not found"]}), 400
        
        # Create new appearance
        new_appearance = Appearance(
            rating=data['rating'],
            episode_id=data['episode_id'],
            guest_id=data['guest_id']
        )
        
        db.session.add(new_appearance)
        db.session.commit()
        
        # Return the created appearance with related data
        appearance_data = new_appearance.to_dict(only=('id', 'rating', 'guest_id', 'episode_id', 'episode', 'guest'))
        return jsonify(appearance_data), 201
        
    except IntegrityError as e:
        db.session.rollback()
        # Check if it's a rating constraint violation
        if 'rating_range_check' in str(e):
            return jsonify({"errors": ["Rating must be between 1 and 5"]}), 400
        else:
            return jsonify({"errors": ["Database constraint violation"]}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400

if __name__ == '__main__':
    app.run(debug=True)