"""Routes for parent Flask app."""
from flask import current_app as app
from flask import render_template, request
from wsgi import mongo

from Predilectura.data.etl import get_readings_stats, get_events_stats


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

    total_records = mongo.db.events.count()
    number_of_records = 10
    total_pages = int(total_records/10) + 1
    current_page = int(request.args.get('page', default=1))
    number_to_skip = number_of_records * (current_page-1)

    data = list(mongo.db.events.find().skip(number_to_skip).limit(number_of_records))
    return render_template('lista_events.jinja2', events=data, prev=current_page-1, current=current_page,
                           next=current_page+1, total_pages=total_pages)

@app.route("/listar_readings")
def lista_readings():

    """
    Page which list reading collection from db
    """

    total_records = mongo.db.readings.count()
    number_of_records = 10
    total_pages = int(total_records / 10) + 1
    current_page = int(request.args.get('page', default=1))
    number_to_skip = number_of_records * (current_page-1)


    # convert the mongodb object to a list
    data = list(mongo.db.readings.find().skip(number_to_skip).limit(number_of_records))

    return render_template('lista_readings.jinja2', readings=data, prev=current_page-1, current=current_page,
                           next=current_page+1, total_pages=total_pages)



@app.route("/listar_ABT")
def lista_ABT():

    """
    Page which list reading collection from db
    """

    total_records = mongo.db.abt.count()
    number_of_records = 10
    total_pages = int(total_records / 10) + 1
    current_page = int(request.args.get('page', default=1))
    number_to_skip = number_of_records * (current_page-1)


    # convert the mongodb object to a list
    data = list(mongo.db.abt.find().skip(number_to_skip).limit(number_of_records))

    return render_template('lista_abt.jinja2', abt=data, prev=current_page-1, current=current_page,
                           next=current_page+1, total_pages=total_pages)


@app.route("/generar_abt")
def generar_abt():

    """
    Page where you are able to select the field which will be part of the analytics base table
    """
    # List of users
    #lst_users = [2074459, 2074562, 2074565]
    lst_users = mongo.db.readings.distinct("user_id")

    # Collection name
    collection_abt = mongo.db["abt"]

    # drop collection col1
    collection_abt.drop()

    for user in lst_users:

        # Get readings data by user
        result_readings = get_readings_stats(user)
        user_data = []
        for result in result_readings:
            dict_user = {
                "user_id": result["_id"]["user_id"],
                "book": result["_id"]["edition_id"],
                "language": result["_id"]["edition_language"],
                "min_percent": result["min_percent"],
                "max_percent": result["max_percent"],
                "avg_percent": result["avg_percent"],
                "max_words": result["max_words"],
                "min_words": result["min_words"],
                "avg_words": result["avg_words"],
                "premium": result["avg_words"],
                "devices_readings": len(result["devices"]),
                "versions_readings": len(result["versions"]),
                "chapters_readings": len(result["chapters"]),
                "event_classes": 0,
                "event_objs": 0,
                "event_types": 0,
                "devices_events": 0,
                "versions_events": 0,
                "chapters_events": 0
            }
            user_data.append(dict_user)

        # Get events data by user
        result_events = get_events_stats(user)

        for result in result_events:

            # Find this data in readings to update, if not create a new one
            element_found =None
            for element in user_data:
                if element["user_id"] == result["_id"]["user_id"] and element["book"] == result["_id"]["edition_id"] \
                        and element["language"] == result["_id"]["edition_language"]:
                    element_found = element
                    break

            if element_found is None:
                dict_user = {
                    "user_id": result["_id"]["user_id"],
                    "book": result["_id"]["edition_id"],
                    "language": result["_id"]["edition_language"],
                    "min_percent": 0,
                    "max_percent": 0,
                    "avg_percent": 0,
                    "max_words": 0,
                    "avg_words": 0,
                    "premium": 0,
                    "devices_readings": 0,
                    "versions_readings": 0,
                    "chapters_readings": 0,
                    "event_classes": result["event_classes"],
                    "event_objs": result["event_objs"],
                    "event_types": len(result["event_types"]),
                    "devices_events": len(result["devices"]),
                    "versions_events": len(result["versions"]),
                    "chapters_events": len(result["chapters"]),
                }
                user_data.append(dict_user)
            else:
                element_found["event_classes"] = result["event_classes"],
                element_found["event_objs"] = result["event_objs"],
                element_found["event_types"] = len(result["event_types"]),
                element_found["devices_events"] = len(result["devices"]),
                element_found["versions_events"] = len(result["versions"]),
                element_found["chapters_events"] = len(result["chapters"])

        for element in user_data:
            collection_abt.insert(element)


    return render_template('generar_abt.jinja2')


@app.route("/create_abt")
def create_abt():

    """
    Create the analytics base table from selected fields before
    """

    # List of users
    mongo.db.readings.find().distinct("user_id")


    return render_template('generar_abt.jinja2')