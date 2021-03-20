"""Routes for parent Flask app."""
from flask import current_app as app
from flask import render_template, request
from wsgi import mongo

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
    data = list(mongo.db.reading.find().skip(number_to_skip).limit(number_of_records))

    return render_template('lista_reading.jinja2', reading=data, prev=current_page -1, next=current_page +1)

@app.route("/generar_abt")
def generar_abt():

    """
    Page where ou are able to select the field which will be part of the analytics base table
    """

    return render_template('generar_abt.jinja2')
