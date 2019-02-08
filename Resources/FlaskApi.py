import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
# Chris to look into why we get errors when not using the check_same_thread arg
engine = create_engine("sqlite:///hawaii.sqlite", connect_args={'check_same_thread':False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}
#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():

    
    results = session.query(Measurement).all()
    
    all_measurements = []
    for measurement in results:
        measurement_dict = {}
        measurement_dict["id"] = measurement.id
        measurement_dict["station"] = measurement.station
        measurement_dict["date"] = measurement.date
        measurement_dict["prcp"] = measurement.prcp
        measurement_dict["tobs"] = measurement.tobs
        all_measurements.append(measurement_dict)

    return jsonify(all_measurements)

@app.route("/api/v1.0/stations")
def stations():

    
    results = session.query(Station).all()
    
    all_stations = []
    for station in results:
        station_dict = {}
        station_dict["id"] = station.id
        station_dict["station"] = station.station
        station_dict["name"] = station.name
        station_dict["latitude"] = station.latitude
        station_dict["longitude"] = station.longitude
        station_dict["elevation"] = station.elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)


@app.route("/api/v1.0/stations")
def passengers():
    
    results = session.query(Passenger).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_passengers = []
    for passenger in results:
        passenger_dict = {}
        passenger_dict["name"] = passenger.name
        passenger_dict["age"] = passenger.age
        passenger_dict["sex"] = passenger.sex
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)