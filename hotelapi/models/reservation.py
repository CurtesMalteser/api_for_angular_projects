from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

db = SQLAlchemy()

class Reservation(db.Model):

    __tablename__ = 'reservation'

    id = db.Column(db.Integer, primary_key=True)
    checkInDate = db.Column(db.DateTime, nullable=False)
    checkOutDate = db.Column(db.DateTime, nullable=False)
    guestName = db.Column(db.String(120))
    guestEmail = db.Column(db.String(120))
    roomNumber = db.Column(db.Integer)


@dataclass
class ReservationData():
    id : int
    checkInDate : str
    checkOutDate : str
    guestName : str
    guestEmail : str
    roomNumber : int

    def __init__(self, id: int, checkInDate: str, checkOutDate: str, guestName: str, guestEmail: str, roomNumber: int):
        self.id = id
        self.checkInDate = checkInDate
        self.checkOutDate = checkOutDate
        self.guestName = guestName
        self.guestEmail = guestEmail
        self.roomNumber = roomNumber

    @classmethod
    def fromReservation(cls, model: Reservation):
        return cls(
            id = model.id,
            checkInDate = str(model.checkInDate),
            checkOutDate = str(model.checkOutDate),
            guestName = model.guestName,
            guestEmail = model.guestEmail,
            roomNumber = model.roomNumber,
        )
