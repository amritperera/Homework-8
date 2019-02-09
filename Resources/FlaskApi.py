import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect
import datetime as dt

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
# Setting up some functions
#################################################
#gets latest date
def get_last_date():
    l_date = []
    latest_date = session.query(func.max(Measurement.date))

    for date in latest_date:
        date_dict = {}
        date_dict['date'] = date
        l_date.append(date_dict)

    return l_date[0]['date'][0]

def calc_temps(start_date, end_date):

    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

#################################################

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

@app.route("/api/v1.0/tobs")
def tobs():
    x = get_last_date()

    results = session.query(Measurement).filter(Measurement.date.between (dt.datetime.strptime(x,'%Y-%m-%d')+dt.timedelta(-365),dt.datetime.strptime(x,'%Y-%m-%d')))
    
    all_measurements = []
    for measurement in results:
        measurement_dict = {}
        measurement_dict["date"] = measurement.date
        measurement_dict["tobs"] = measurement.tobs
        all_measurements.append(measurement_dict)

    return jsonify(all_measurements)

@app.route("/api/v1.0/<start>")
def start_only(start):
    x = get_last_date()
    calculations = calc_temps(start,x)

    start_o = list(np.ravel(calculations))


    return jsonify(start_o)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    calculations = calc_temps(start,end)

    start_o = list(np.ravel(calculations))


    return jsonify(start_o)


if __name__ == '__main__':
    app.run(debug=True)
