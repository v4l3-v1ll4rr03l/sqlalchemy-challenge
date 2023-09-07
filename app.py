# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
    return "hey"

@app.route("/api/v1.0/stations")
def stations():
    return "hi"

@app.route("/api/v1.0/tobs")
def tobs():
    return "hi"

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