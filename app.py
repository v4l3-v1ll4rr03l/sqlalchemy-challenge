# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np

#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
base = automap_base()

# reflect the tables
base.prepare(autoload_with=engine)

# Save references to each table
measurement = base.classes.measurement
station = base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Helper function for queries
def cut_off_date():
    dates = session.query(measurement.date)
    recent = dates[0]
    for date in dates:
        if recent < date:
            recent = date
    date = recent[0].split("-")
    date = dt.datetime(int(date[0]), int(date[1]), int(date[2]))
    cut_off = date - dt.timedelta(days=365)
    return cut_off


#################################################
# Flask Setup
#################################################


app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/'enter start date'<br/>"
        f"/api/v1.0/'enter start date'/'enter end date'<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    cut_off = cut_off_date()
    precipitation_data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= cut_off).all()
    
    precipitation_dict = {}

    for date, precipitation in precipitation_data:
        precipitation_dict[date] = precipitation

    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    station_names = session.query(station.name).all()
    station_list= list(np.ravel(station_names))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    cut_off = cut_off_date()
    station_counts = session.query(measurement.station, func.count(measurement.prcp)).group_by(measurement.station).order_by(func.count(measurement.prcp).desc()).all()
    most_active = station_counts[0][0]
    temp_data = session.query(measurement.tobs).filter(measurement.station == most_active).filter(measurement.date >= cut_off).all()
    temp_list = list(np.ravel(temp_data))
    return jsonify(temp_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def tobs_date_range(start, end=None):
    if end:
        result = "hi"
    else:
        result = "hey"
    return result

if __name__ == '__main__':
    app.run(debug=True)

session.close()