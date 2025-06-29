#!/usr/bin/env python3
from app import app
from models import db, Episode, Guest, Appearance
from datetime import datetime

def seed_data():
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        Appearance.query.delete()
        Guest.query.delete()
        Episode.query.delete()
        
        # Create Episodes
        print("Creating episodes...")
        episodes = [
            Episode(date="1/11/99", number=1),
            Episode(date="1/12/99", number=2),
            Episode(date="1/13/99", number=3),
            Episode(date="1/14/99", number=4),
            Episode(date="1/15/99", number=5),
            Episode(date="1/18/99", number=6),
            Episode(date="1/19/99", number=7),
            Episode(date="1/20/99", number=8),
        ]
        
        for episode in episodes:
            db.session.add(episode)
        
        # Create Guests
        print("Creating guests...")
        guests = [
            Guest(name="Wycliffe Oparanya", occupation="politician"),
            Guest(name="Lupita Nyong'o", occupation="actress"),
            Guest(name="Eliud Kipchoge", occupation="marathon runner"),
            Guest(name="Marcus Rashford", occupation="footballer"),
            Guest(name="Catherine Ndereba", occupation="marathon runner"),
            Guest(name="Bruno Fernandes", occupation="footballer"),
            Guest(name="Raila Odinga", occupation="liberator"),
            Guest(name="Jadon Sancho", occupation="footballer"),
            Guest(name="Wangari Maathai", occupation="environmentalist"),
            Guest(name="Harry Maguire", occupation="footballer"),
        ]
        
        for guest in guests:
            db.session.add(guest)
        
        # Commit episodes and guests first to get their IDs
        db.session.commit()
        
        # Create Appearances
        print("Creating appearances...")
        appearances = [
            Appearance(rating=4, episode_id=1, guest_id=1), 
            Appearance(rating=5, episode_id=1, guest_id=4),  
            Appearance(rating=3, episode_id=2, guest_id=3),  
            Appearance(rating=5, episode_id=2, guest_id=5),  
            Appearance(rating=4, episode_id=3, guest_id=2),  
            Appearance(rating=4, episode_id=3, guest_id=6), 
            Appearance(rating=5, episode_id=4, guest_id=7),  
            Appearance(rating=3, episode_id=4, guest_id=9),  
            Appearance(rating=5, episode_id=5, guest_id=10), 
            Appearance(rating=4, episode_id=5, guest_id=1),  
            Appearance(rating=4, episode_id=6, guest_id=8),  
            Appearance(rating=5, episode_id=6, guest_id=4),  
            Appearance(rating=3, episode_id=7, guest_id=2),  
            Appearance(rating=4, episode_id=7, guest_id=5),  
            Appearance(rating=5, episode_id=8, guest_id=6),  
            Appearance(rating=4, episode_id=8, guest_id=9), 
        ]
        
        for appearance in appearances:
            db.session.add(appearance)
        
        # Commit all appearances
        db.session.commit()
        
        print("Seed data created successfully!")
        print(f"Created {len(episodes)} episodes")
        print(f"Created {len(guests)} guests")
        print(f"Created {len(appearances)} appearances")

if __name__ == "__main__":
    seed_data()
