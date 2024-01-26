from flask import (
    Flask,
    jsonify
    )
from flask_migrate import Migrate
from hotelapi.models.reservation import *
from datetime import datetime
import hotelapi.config as config

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config)

    db.init_app(app)

    migrate = Migrate(app, db)

    # a simple page that says hello
    @app.route('/reservations')
    def getReservations():
        reservation = ReservationData()
        reservation.id = 1
        reservation.checkInDate = str(datetime.now())
        reservation.checkOutDate = str(datetime.now())
        reservation.guestName = 'Test'
        reservation.guestEmail = 'test@email.com'
        reservation.roomNumber = 1

        reservation2 = ReservationData()
        reservation2.id = 2
        reservation2.checkInDate = str(datetime.now())
        reservation2.checkOutDate = str(datetime.now())
        reservation2.guestName = 'Test2'
        reservation2.guestEmail = 'test2@email.com'
        reservation2.roomNumber = 2


        

        users = '[{}]'.format(reservation.toJSON() + ', ' + reservation2.toJSON())
        return jsonify(users) 

    return app