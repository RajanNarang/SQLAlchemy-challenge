from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify



engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
measurements = Base.classes.measurement
stations = Base.classes.station
session = Session(engine)
app = Flask(__name__)

@app.route("/")

def homepage():
    return("The available routes are: <br>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>")


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last year"""
    last_year_date = dt.date(2016, 8, 23)
    
    data = session.query(measurements.date, measurements.prcp).filter(measurements.date >= last_year_date).all()
    date_list = []
    prcp_list = []
    for items in data:
        date_list.append(items[0])
        prcp_list.append(items[1])
    precipation_dict = {}
    precipation_dict['date'] = date_list
    precipation_dict['prcp'] = prcp_list
    
    return jsonify(precipation_dict)
    


   


@app.route("/api/v1.0/stations")
def stations():    
    station_list = session.query(measurements.station,func.count(measurements.station)).group_by(measurements.station).order_by(func.count(measurements.station).desc()).all()

    
    station_dict = {}
    station_dict['station'] = station_list
    
    return jsonify(station_dict)
    


@app.route("/api/v1.0/tobs")
def temp_monthly():
    
    last_year_date = dt.date(2016, 8, 23)
    temps = session.query(measurements.tobs).filter(measurements.station == 'USC00519281').filter(measurements.date >= last_year_date).all()
    tobs = list(np.ravel(temps))

    return jsonify(temperature=tobs)


if __name__ == '__main__':
    app.run()