from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checkInDate = db.Column(db.DateTime, nullable=False)
    checkOutDate = db.Column(db.DateTime, nullable=False)
    guestName = db.Column(db.String(120))
    guestEmail = db.Column(db.String(120))
    roomNumber = db.Column(db.Integer)