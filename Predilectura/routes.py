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

    # get headers
    dict_header = dict()
    dict_header["user_id"] = True
    dict_header["book"] = True
    dict_header["language"] = True
    dict_header["min_percent"] = False
    dict_header["max_percent"] = False
    dict_header["avg_percent"] = False
    dict_header["max_words"] = False
    dict_header["min_words"] = False
    dict_header["avg_words"] = False
    dict_header["premium"] = False
    dict_header["devices_readings"] = False
    dict_header["versions_readings"] = False
    dict_header["chapters_readings"] = False
    dict_header["event_classes"] = False
    dict_header["event_objs"] = False
    dict_header["event_types"] = False
    dict_header["devices_events"] = False
    dict_header["versions_events"] = False
    dict_header["chapters_events"] = False

    firstElement = mongo.db.abt.find_one()

    if "min_percent" in firstElement:
        dict_header["min_percent"] = True

    if "max_percent" in firstElement:
        dict_header["max_percent"] = True

    if "avg_percent" in firstElement:
        dict_header["avg_percent"] = True

    if "max_words" in firstElement:
        dict_header["max_words"] = True

    if "min_words" in firstElement:
        dict_header["min_words"] = True

    if "avg_words" in firstElement:
        dict_header["avg_words"] = True

    if "premium" in firstElement:
        dict_header["premium"] = True

    if "devices_readings" in firstElement:
        dict_header["devices_readings"] = True

    if "versions_readings" in firstElement:
        dict_header["versions_readings"] = True

    if "chapters_readings" in firstElement:
        dict_header["chapters_readings"] = True

    if "event_classes" in firstElement:
        dict_header["event_classes"] = True

    if "event_objs" in firstElement:
        dict_header["event_objs"] = True

    if "event_types" in firstElement:
        dict_header["event_types"] = True

    if "devices_events" in firstElement:
        dict_header["devices_events"] = True

    if "versions_events" in firstElement:
        dict_header["versions_events"] = True

    if "chapters_events" in firstElement:
        dict_header["chapters_events"] = True

    # convert the mongodb object to a list
    data = list(mongo.db.abt.find().skip(number_to_skip).limit(number_of_records))

    return render_template('lista_abt.jinja2', abt=data, prev=current_page-1, current=current_page,
                           next=current_page+1, total_pages=total_pages, header=dict_header)


@app.route("/generar_abt")
def generar_abt():

    """
    Page where you are able to select the field which will be part of the analytics base table
    """

    return render_template('generar_abt.jinja2')


@app.route("/create_abt", methods=["POST"])
def create_abt():

    """
    Create the analytics base table from selected fields before
    """
    dict_abt_features = dict()
    dict_abt_features["user_id"] = True
    dict_abt_features["book"] = True
    dict_abt_features["language"] = True
    dict_abt_features["min_percent"] = True if request.form.get("min_percent") is not None else False
    dict_abt_features["max_percent"] = True if request.form.get("max_percent") is not None else False
    dict_abt_features["avg_percent"] = True if request.form.get("avg_percent") is not None else False
    dict_abt_features["max_words"] = True if request.form.get("max_words") is not None else False
    dict_abt_features["min_words"] = True if request.form.get("min_words") is not None else False
    dict_abt_features["avg_words"] = True if request.form.get("avg_words") is not None else False
    dict_abt_features["premium"] = True if request.form.get("premium") is not None else False
    dict_abt_features["devices_readings"] = True if request.form.get("devices_readings") is not None else False
    dict_abt_features["versions_readings"] = True if request.form.get("versions_readings") is not None else False
    dict_abt_features["chapters_readings"] = True if request.form.get("chapters_readings") is not None else False
    dict_abt_features["event_classes"] = True if request.form.get("event_classes") is not None else False
    dict_abt_features["event_objs"] = True if request.form.get("event_objs") is not None else False
    dict_abt_features["event_types"] = True if request.form.get("event_types") is not None else False
    dict_abt_features["devices_events"] = True if request.form.get("devices_events") is not None else False
    dict_abt_features["versions_events"] = True if request.form.get("versions_events") is not None else False
    dict_abt_features["chapters_events"] = True if request.form.get("chapters_events") is not None else False

    # List of users
    # lst_users = [2074459, 2074562, 2074565]
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
                "language": result["_id"]["edition_language"]}

            if dict_abt_features["min_percent"] is True:
                dict_user["min_percent"] = result["min_percent"]

            if dict_abt_features["max_percent"] is True:
                dict_user["max_percent"] = result["max_percent"]

            if dict_abt_features["avg_percent"] is True:
                dict_user["avg_percent"] = result["avg_percent"]

            if dict_abt_features["max_words"] is True:
                dict_user["max_words"] = result["max_words"]

            if dict_abt_features["min_words"] is True:
                dict_user["min_words"] = result["min_words"]

            if dict_abt_features["avg_words"] is True:
                dict_user["avg_words"] = result["avg_words"]

            if dict_abt_features["premium"] is True:
                dict_user["premium"] = result["premium"]

            if dict_abt_features["devices_readings"] is True:
                dict_user["devices_readings"] = len(result["devices"])

            if dict_abt_features["versions_readings"] is True:
                dict_user["versions_readings"] = len(result["versions"])

            if dict_abt_features["chapters_readings"] is True:
                dict_user["chapters_readings"] = len(result["chapters"])

            if dict_abt_features["event_classes"] is True:
                dict_user["event_classes"] = 0

            if dict_abt_features["event_objs"] is True:
                dict_user["event_objs"] = 0

            if dict_abt_features["event_types"] is True:
                dict_user["event_types"] = 0

            if dict_abt_features["devices_events"] is True:
                dict_user["devices_events"] = 0

            if dict_abt_features["versions_events"] is True:
                dict_user["versions_events"] = 0

            if dict_abt_features["chapters_events"] is True:
                dict_user["chapters_events"] = 0

            user_data.append(dict_user)

        # Get events data by user
        result_events = get_events_stats(user)

        for result in result_events:

            # Find this data in readings to update, if not create a new one
            element_found = None
            for element in user_data:
                if element["user_id"] == result["_id"]["user_id"] and element["book"] == result["_id"]["edition_id"] \
                        and element["language"] == result["_id"]["edition_language"]:
                    element_found = element
                    break

            if element_found is None:
                dict_user = {
                    "user_id": result["_id"]["user_id"],
                    "book": result["_id"]["edition_id"],
                    "language": result["_id"]["edition_language"]

                }

                if dict_abt_features["min_percent"] is True:
                    dict_user["min_percent"] = 0

                if dict_abt_features["max_percent"] is True:
                    dict_user["max_percent"] = 0

                if dict_abt_features["avg_percent"] is True:
                    dict_user["avg_percent"] = 0

                if dict_abt_features["max_words"] is True:
                    dict_user["max_words"] = 0

                if dict_abt_features["min_words"] is True:
                    dict_user["min_words"] = 0

                if dict_abt_features["avg_words"] is True:
                    dict_user["avg_words"] = 0

                if dict_abt_features["premium"] is True:
                    dict_user["premium"] = 0

                if dict_abt_features["devices_readings"] is True:
                    dict_user["devices_readings"] = 0

                if dict_abt_features["versions_readings"] is True:
                    dict_user["versions_readings"] = 0

                if dict_abt_features["chapters_readings"] is True:
                    dict_user["chapters_readings"] = 0

                if dict_abt_features["event_classes"] is True:
                    dict_user["event_classes"] = result["event_classes"]

                if dict_abt_features["event_objs"] is True:
                    dict_user["event_objs"] = result["event_objs"]

                if dict_abt_features["event_types"] is True:
                    dict_user["event_types"] = len(result["event_types"])

                if dict_abt_features["devices_events"] is True:
                    dict_user["devices_events"] = len(result["devices"])

                if dict_abt_features["versions_events"] is True:
                    dict_user["versions_events"] = len(result["versions"])

                if dict_abt_features["chapters_events"] is True:
                    dict_user["chapters_events"] = len(result["chapters"])

                user_data.append(dict_user)
            else:

                if dict_abt_features["event_classes"] is True:
                    element_found["event_classes"] = result["event_classes"]

                if dict_abt_features["event_objs"] is True:
                    element_found["event_objs"] = result["event_objs"]

                if dict_abt_features["event_types"] is True:
                    element_found["event_types"] = len(result["event_types"])

                if dict_abt_features["devices_events"] is True:
                    element_found["devices_events"] = len(result["devices"])

                if dict_abt_features["versions_events"] is True:
                    element_found["versions_events"] = len(result["versions"])

                if dict_abt_features["chapters_events"] is True:
                    element_found["chapters_events"] = len(result["chapters"])

        for element in user_data:
            collection_abt.insert(element)

    return render_template('lista_datos.jinja2')
