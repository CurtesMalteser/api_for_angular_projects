from flask import (
    Flask,
    jsonify,
    request,
    abort,
    )
from flask_migrate import Migrate
from flask_cors import (
    CORS,
    cross_origin,
    )
from hotelapi.models.reservation import *
from datetime import datetime
import hotelapi.config as config
import json

import sys
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

        reservations = Reservation.query.all()
        
        reservations = map(lambda reservation : ReservationData(
            id = reservation.id,
            checkInDate = str(reservation.checkInDate),
            checkOutDate = str(reservation.checkOutDate),
            guestName = reservation.guestName,
            guestEmail = reservation.guestEmail,
            roomNumber = reservation.roomNumber,
        ), reservations)

        return jsonify(list(reservations))

    @app.route('/reservation/<int:id>')
    @cross_origin()
    def getReservation(id: int):

        try:
            reservation = Reservation.query.get(id)
            reservation = ReservationData.fromReservation(model=reservation)

            return jsonify(reservation)
        except:
            #TODO: handle gracefuly with error code, also if the Reservation.query.get(id) just return 200 empty JSON
            return jsonify('')

    @app.route('/reservation', methods=['POST'])
    @cross_origin()
    def setReservation():
        content_type = request.headers.get('Content-Type')
        if ('application/json' in content_type):
            try:
                json_data = json.dumps(request.json)
                reservation = json.loads(json_data, object_hook =
                   lambda d : Reservation(
                        checkInDate= str(d.get('checkInDate')),
                        checkOutDate= str(d.get('checkOutDate')),
                        guestName= str(d.get('guestName')),
                        guestEmail= str(d.get('guestEmail')),
                        roomNumber= str(d.get('roomNumber')),
                        ))
    
                db.session.add(reservation)
                db.session.commit()
            except:
                db.session.rollback()
            finally:
                db.session.close()

            return jsonify(request.json)

        else:
            abort(404, "Content type is not supported.")

    @app.route('/reservation/<int:id>', methods=['DELETE'])
    @cross_origin()
    def deleteReservation(id: int):

        error = False

        try:
            reservation = Reservation.query.get(id)
            db.session.delete(reservation)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()
        
        if(error):
            abort(500)
        else:
           return jsonify("")

    return app