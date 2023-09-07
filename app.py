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

# queries and processing to obtain cut off date for one year's worth of data
session = Session(engine)
dates = session.query(measurement.date)
recent = dates[0]
for date in dates:
    if recent < date:
        recent = date
date = recent[0].split("-")
date = dt.datetime(int(date[0]), int(date[1]), int(date[2]))
cut_off = date - dt.timedelta(days=365)
session.close()

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
        f"/api/v1.0/'yyyy-mm-dd'<br/>"
        f"/api/v1.0/'yyyy-mm-dd'/'yyyy-mm-dd'<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    precipitation_data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= cut_off).all()
    precipitation_dict = {}

    for date, precipitation in precipitation_data:
        precipitation_dict[date] = precipitation

    session.close()
    return jsonify(precipitation_dict)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    station_names = session.query(station.name).all()
    station_list= list(np.ravel(station_names))

    session.close()
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    station_counts = session.query(measurement.station, func.count(measurement.prcp)).group_by(measurement.station).order_by(func.count(measurement.prcp).desc()).all()
    most_active = station_counts[0][0]
    temp_data = session.query(measurement.date, measurement.tobs).filter(measurement.station == most_active).filter(measurement.date >= cut_off).all()
    temp_dict = {}

    for date, tobs in temp_data:
        temp_dict[date] = tobs

    session.close()
    return jsonify(temp_dict)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def tobs_date_range(start, end=None):
    session = Session(engine)

    tobs_data = []
    temp = start.split("-")
    start_date = dt.datetime(int(temp[0]), int(temp[1]), int(temp[2]))

    if end:
        temp = end.split("-")
        end_date = dt.datetime(int(temp[0]), int(temp[1]), int(temp[2]))
        tobs_data = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(start_date <= measurement.date).filter(measurement.date <= end_date).all()
    else:
        tobs_data = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start_date).all()
   
    tobs_list = list(np.ravel(tobs_data))

    session.close()
    return jsonify(tobs_list)


if __name__ == '__main__':
    app.run(debug=True)