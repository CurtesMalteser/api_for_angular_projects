from flask import (
    Flask,
    jsonify
    )
from flask_migrate import Migrate
from flask_cors import (
    CORS,
    cross_origin,
    )
from hotelapi.models.reservation import *
from datetime import datetime
import hotelapi.config as config

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)

    migrate = Migrate(app, db)

    @app.route('/reservations')
    @cross_origin()
    def getReservations():
        reservation = ReservationData()
        reservation.id = 1
        reservation.checkInDate = '2024-01-27'
        reservation.checkOutDate = '2024-01-28'
        reservation.guestName = 'Test'
        reservation.guestEmail = 'test@email.com'
        reservation.roomNumber = 1

        reservation2 = ReservationData()
        reservation2.id = 2
        reservation2.checkInDate = '2024-01-30'
        reservation2.checkOutDate = '2024-02-02'
        reservation2.guestName = 'Test2'
        reservation2.guestEmail = 'test2@email.com'
        reservation2.roomNumber = 2

        reservations = '[{}]'.format(reservation.toJSON() + ', ' + reservation2.toJSON())
        return reservations

    @app.route('/reservation/<int:id>')
    @cross_origin()
    def getReservation(id: int):

        reservation = ReservationData()
        reservation.id = 1
        reservation.checkInDate = '2024-01-27'
        reservation.checkOutDate = '2024-01-27'
        reservation.guestName = 'Test'
        reservation.guestEmail = 'test@email.com'
        reservation.roomNumber = 1

        return reservation.toJSON()

    return app