from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checkInDate = db.Column(db.DateTime, nullable=False)
    checkOutDate = db.Column(db.DateTime, nullable=False)
    guestName = db.Column(db.String(120))
    guestEmail = db.Column(db.String(120))
    roomNumber = db.Column(db.Integer)

class ReservationData():
    id : int
    checkInDate : str
    checkOutDate : str
    guestName : str
    guestEmail : str
    roomNumber : int

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)