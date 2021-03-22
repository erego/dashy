"""Routes for parent Flask app."""
from flask import current_app as app
from flask import render_template, request
from wsgi import mongo

from Predilectura.data.etl import get_reading_stats

@app.route("/")
def home():
    """Landing page."""

    return render_template(
        "index.jinja2",
        title="Plotly Dash Flask Tutorial",
        description="Embed Plotly Dash into your Flask applications.",
        template="home-template",
        body="This is a homepage served with Flask.",
    )


@app.route("/datos")
def lista_datos():

    """
    Page which list different types of data to work with
    """
    return render_template(
        "lista_datos.jinja2"
    )

@app.route("/listar_events")
def lista_events():

    """
    Page which list events collection from db
    """
    number_of_records = 10
    current_page = int(request.args.get('page', default=0))
    number_to_skip = number_of_records * current_page


    data = list(mongo.db.events.find().skip(number_to_skip).limit(number_of_records))
    return render_template('lista_events.jinja2', events=data, prev=current_page -1, next=current_page +1)

@app.route("/listar_reading")
def lista_reading():

    """
    Page which list reading collection from db
    """

    number_of_records = 10
    current_page = int(request.args.get('page', default=0))
    number_to_skip = number_of_records * current_page


    # convert the mongodb object to a list
    data = list(mongo.db.readings.find().skip(number_to_skip).limit(number_of_records))

    return render_template('lista_reading.jinja2', readings=data, prev=current_page -1, next=current_page +1)


@app.route("/generar_abt")
def generar_abt():

    """
    Page where you are able to select the field which will be part of the analytics base table
    """
    # List of users

    # TODO undo mongo db consult
    lst_users = [2074459, 2074562, 2074565]

    for user in lst_users:
        # Get readings data by user
        result_readings = get_readings_stats(user)

        for result in result_readings:
            print(result)

        # Get events data by user
        result_readings = get_events_stats(user)

        for result in result_readings:
            print(result)

        a = 5

    #lst_users = mongo.db.readings.distinct("user_id")


    return render_template('generar_abt.jinja2')

@app.route("/create_abt")
def create_abt():

    """
    Create the analytics base table from selected fields before
    """

    # List of users
    mongo.db.readings.find().distinct("user_id")


    return render_template('generar_abt.jinja2')