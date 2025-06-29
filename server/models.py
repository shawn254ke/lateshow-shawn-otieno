from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, CheckConstraint
from sqlalchemy_serializer import SerializerMixin

# contains definitions of tables and associated schema constructs
metadata = MetaData()

# create the Flask SQLAlchemy extension
db = SQLAlchemy(metadata=metadata)

class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'
    
    # Serialization rules to prevent infinite recursion
    serialize_rules = ('-appearances.episode',)
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(255), nullable=False)
    number = db.Column(db.Integer, nullable=True)
    
    # Relationship with cascade delete
    appearances = db.relationship('Appearance', backref='episode', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Episode {self.number} aired on {self.date}>"
    
class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'
    
    # Serialization rules to prevent infinite recursion
    serialize_rules = ('-episode.appearances', '-guest.appearances')
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id', ondelete='CASCADE'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id', ondelete='CASCADE'), nullable=False)

    # Validation constraint for rating between 1 and 5
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='rating_range_check'),
    )
    
    def __repr__(self):
        return f"<Appearance of {self.guest.name if self.guest else 'Unknown'} on Episode {self.episode_id}>"

class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'
    
    # Serialization rules to prevent infinite recursion
    serialize_rules = ('-appearances.guest',)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    occupation = db.Column(db.String(255), nullable=True)
    
    # Relationship with cascade delete
    appearances = db.relationship('Appearance', backref='guest', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Guest {self.name}>"