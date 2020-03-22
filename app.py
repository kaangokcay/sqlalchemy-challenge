from flask import Flask, jsonify
import datetime as dt 
import numpy as np  
import pandas as pd 
import sqlalchemy  
from sqlalchemy.ext.automap import automap_base 
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Setup SQLite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect database into a new model
Base = automap_base()

# Reflect tables
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session (link) from Python to database
session = Session(engine)


app = Flask(__name__)

@app.route("/")
def home():
    print('Home Page')
    return(
        "Welcome to Hawaii Climate Analysis API!<br/>"
        "Available Routes:<br/>"
        "<a href='/api/v1.0/precipitation'>Precipitation<a/><br/>"
        "<a href='/api/v1.0/stations'>Stations<a/><br/>"
        "<a href='/api/v1.0/tobs'>Tobs<a/><br/>"
        "Select Date: Start Date(Required), End Date(Optional)<br/>"
        "<a href='/api/v1.0/<start>/<end>'>Custom_Dates<a/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    print('Query and Print Precipitation Data')
   
    session = Session(engine)
    results = session.query(Measurement.prcp, Measurement.date).all()
    session.close()

    prcp_dict = {}
    
    for prcp, date in results:
        prcp_dict[date] = prcp
    
    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():
    print('Query and Print Station List')
    
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()

    all_stations = list(np.ravel(results))
    
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    print('Query and Print TOBS List')
    
    session = Session(engine)
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').all()
    session.close()

    return jsonify(tobs_data)


@app.route("/api/v1.0/<start_date>/<end_date>")
def custom_dates(start_date = None, end_date = None):
    print('Query and Print Temperature Data for Custom Dates')

    session = Session(engine)

    if not end_date:        
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).all()
        temps = list(np.ravel(results))
        session.close()
        return jsonify(temps)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    temps = list(np.ravel(results))
    session.close()

    return jsonify(temps)



if __name__ == "__main__":
    app.run(debug=True)