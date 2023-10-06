from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
	#password is never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)
    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user') # backref must match what's in models (comments to comments)

    # string print method
    def __repr__(self):
        return f"Name: {self.name}"

class Destination(db.Model):
    __tablename__ = 'destinations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    currency = db.Column(db.String(3))
    # ... Create the Comments db.relationship
	# relation to call destination.comments and comment.destination
    comments = db.relationship('Comment', backref='destination')
	# string print method
    def __repr__(self):
        return f"Name: {self.name}"
    
# class Genre(db.Model): # For assignment
#     __tablename__ = 'genre'
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String (200))

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    # add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'))

    def __repr__(self):
        return f"Comment: {self.text}"
    
class Hotel(db.Model):
    __tablename__ = 'hotels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, nullable=False)
    description = db.Column(db.String(500))
    room_avail = db.Column(db.Boolean, default=1)
    # Define the one-to-many relationship with the Room model
    rooms = db.relationship('Room', backref='hotel', lazy='dynamic')
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'))

    def to_dict(self):
        h_dict = {
            b.name: str(getattr(self, b.name)) for b in self.__table__.columns
        }
        h_rooms = []
        # Add details of related Rooms to the Hotel's h_dict
        for room in self.rooms:
            room_data = {
                'id': room.id,
                'room_type': room.type,
                'num_rooms': room.num_rooms,
                'room_description': room.description,
                'room_rate': room.rate,
                'hotel_id': room.hotel_id
            }
            h_rooms.append(room_data)
        h_dict['rooms'] = h_rooms
        return h_dict

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), index=True, nullable=False)
    num_rooms = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500))
    rate = db.Column(db.Float(7))
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'))