# Import the dependencies.

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import pandas as pd
import datetime as dt
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
from flask import Flask, jsonify



#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine('sqlite:///hawaii.sqlite')

# Declare a Base using `automap_base()`
base = automap_base()

# Use the Base class to reflect the database tables
base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = base.classes.measurement
Station = base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)



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
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start><br/>'
        f'/api/v1.0/<start>/<end>'

    )


@app.route('/api/v1.0/precipitation')
def precipitation():
    prcp_q = session.query(Measurement.prcp, Measurement.date).filter(Measurement.date > '2016-08-22').all()
    prcp_list = []
    for prcp, date in prcp_q:
        prcp_list.append({
            'prcp' : prcp
            'date' : date
        })
    return jsonify(prcp_list)


@app.route('/api/v1.0/stations')
def stations():
    station_q = session.query(Station.station).all()
    station_list = []
    for station in station_q:
        station_list.append({
            'station' : station
        })
    return jsonify(station_list)


@app.route('/api/v1.0/tobs')
def tobs():
    tobs_q = session.query(Measurement.tobs, Measurement.date).filter(Measurement.date > '2016-08-17').all()
    tobs_list = []
    for tobs, date in tobs_q:
        tobs_list.append({
            'date' : date
            'tobs' : tobs
        })
    return jsonify(tobs_list)


@app.route('/api/v1.0/<start>')
def start_date(start):
    start_date_q = session.query(func.min(Measurement.tobs), \
                                 func.max(Measurement.tobs), func.avg(Measurement.tobs)\
                                ).filter(Measurement.date >= start)
    start_date_list = []
    for TMIN, TMAX, TAVG in start_date_q:
        start_date_list.append({
            'min' : TMIN
            'max' : TMAX
            'avg' : TAVG
        })
    return jsonify(start_date_list)


@app.route('/api/v1.0/<start>/<end>')
def start_date(start, end):
    start_date_q = session.query(func.min(Measurement.tobs), \
                                 func.max(Measurement.tobs), func.avg(Measurement.tobs)\
                                ).filter(Measurement.date >= start and Measurement.date <= end)
    start_end_date_list = []
    for TMIN, TMAX, TAVG in start_date_q:
        start_date_list.append({
            'min' : TMIN
            'max' : TMAX
            'avg' : TAVG
        })
    return jsonify(start_end_date_list)



if __name__ == '__main__':
    app.run(debug=True)






