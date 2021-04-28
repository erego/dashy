"""Routes for parent Flask app."""

from pathlib import Path

from flask import current_app as app
from flask import render_template, request, g, redirect, url_for

from Predilectura.statistics.dataset_abt import DataSetABT

import pandas as pd

from Predilectura import mongo, babel
from Predilectura.statistics.abt import ABTMongoDB, ABTPandas
from Predilectura.statistics.feature import Feature, FeatureContinuous, FeatureCategorical
from Predilectura.mlearning.information_based import CARTAlgorithm
from Predilectura.forms import FormAlgorithm, FormHandlingQuality, FormABT

from Predilectura.mlearning import model


@babel.localeselector
def get_locale():
    if not g.get('lang_code', None):
        g.lang_code = request.accept_languages.best_match(app.config['LANGUAGES'].keys())
    return g.lang_code


@app.url_defaults
def add_language_code(endpoint, values):
    if 'lang_code' in request.args:
        values.setdefault('lang_code', request.args["lang_code"])
    else:
        values.setdefault('lang_code', g.lang_code)


@app.url_value_preprocessor
def pull_lang_code(endpoint, values):

    if values is None and 'lang_code' not in request.args:
        g.lang_code = request.accept_languages.best_match(app.config['LANGUAGES'])
    elif 'lang_code' not in request.args and 'lang_code' not in values:
        g.lang_code = request.accept_languages.best_match(app.config['LANGUAGES'])
    else:
        if 'lang_code' in request.args:
            g.lang_code = request.args.get('lang_code')
        else:
            g.lang_code = values.pop('lang_code')

@app.route("/")
def home():
    """Landing page."""

    return render_template(
        "index.jinja2",
        title="Visualizatio Data",
        description="Embed Plotly Dash into your Flask applications.",
        template="home-template",
        body="This is a homepage served with Flask.",
    )


@app.route("/datos")
# TODO uncomment login_required
#@login_required
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


@app.route("/listar_ABT", defaults={'format_data': "mongodb"})
@app.route('/listar_ABT/<format_data>')
def list_abt(format_data):

    """
    Page which list reading collection from db
    """

    number_of_records = 10
    data = None
    current_page = 0
    total_pages = 0
    dict_header = None

    if format_data == "mongodb":
        total_records = mongo.db.abt.count()
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

    elif format_data == "pandas":
        path_to_data = Path(app.root_path).joinpath("data", "abt.csv")

        data = pd.read_csv(path_to_data.as_posix())

        total_records = data.shape[0]
        total_pages = int(total_records / 10) + 1
        current_page = int(request.args.get('page', default=1))
        number_to_skip = number_of_records * (current_page - 1)
        data = data[number_to_skip:number_to_skip + number_of_records]
        lst_columns = list(data.columns)
        dict_header = dict.fromkeys(lst_columns, True)

        data = data.to_dict('records')

    return render_template('lista_abt.jinja2', abt=data, prev=current_page-1, current=current_page,
                           next=current_page+1, total_pages=total_pages, header=dict_header, format_data=format_data)


@app.route("/generar_abt")
def generar_abt():

    """
    Page where you are able to select the field which will be part of the analytics base table
    """
    form = FormABT()
    return render_template('generar_abt.jinja2', form=form)


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

    if request.form.get("output_format") == "pandas":
        abt_to_create = ABTPandas(dict_abt_features)
        abt_to_create.create_ABT()
    elif request.form.get("output_format") == "mongodb":
        abt_to_create = ABTMongoDB(dict_abt_features)
        abt_to_create.create_ABT()
    return render_template('lista_datos.jinja2')


@app.route("/calidad_abt", defaults={'format_data': "mongodb"})
@app.route('/calidad_abt/<format_data>')
def quality_abt(format_data):

    data_continuous = None
    data_categorical = None

    if format_data == "mongodb":
        pass
    elif format_data == "pandas":

        path_to_data = Path(app.root_path).joinpath("data", "abt.csv")

        data = pd.read_csv(path_to_data.as_posix())

        total_records = data.shape[0]

        dict_quality_continuous = dict()
        dict_quality_categorical = dict()

        for column in data.columns:

            if column == "user_id":
                continue

            # If cardinality of feature is 1 we discard this column
            if Feature.check_cardinality_one(data[column]):
                continue

            if Feature.check_type(data[column]) == "Continuous":
                feature = FeatureContinuous(column)
                try:
                    dict_quality_continuous[column] = feature.get_statistics(data[column])

                except Exception as excp:
                    a = 5

            elif Feature.check_type(data[column]) == "Categorical":
                feature = FeatureCategorical(column)
                try:
                    dict_quality_categorical[column] = feature.get_statistics(data[column])
                except Exception as excp:
                    a = 5

    return render_template('calidad_abt.jinja2', data_continuous=dict_quality_continuous,
                           data_categorical=dict_quality_categorical)

@app.route('/gestion_calidad_abt')
def handling_quality_abt():
    form = FormHandlingQuality()

    path_to_data = Path(app.root_path).joinpath("data", "abt.csv")

    columns = pd.read_csv(path_to_data.as_posix(), index_col=0, nrows=0).columns.tolist()

    form.features_select.choices = [(column, column) for column in columns]

    return render_template('gestion_calidad_abt.jinja2', form=form)

@app.route("/handle_quality_issues", methods=["POST"])
def handle_quality_issues():
    #TODO crear una columna binaria para decir si un valor está o no está en caso de que haya mucho nan
    selected_option = request.form.get("handler")
    lst_features = request.form.getlist("features_select")
    path_to_data = Path(app.root_path).joinpath("data", "abt.csv")
    dataset_abt = DataSetABT(path_to_data.as_posix())
    if selected_option == "drop_features":
        dataset_abt.drop_features(lst_features)
    elif selected_option == "complete_case":
        dataset_abt.complete_case_analysis()
    elif selected_option == "imputation":
        dataset_abt.imputation(lst_features, request.form.get("imputation"))
    elif selected_option == "clamp":
        dataset_abt.clamp(lst_features)

    return redirect(url_for('quality_abt', format_data="pandas"))
    return render_template('lista_datos.jinja2')

@app.route('/algorithm_train')
def algorithm_train():

    form = FormAlgorithm()
    return render_template('algorithm_train.jinja2', form=form)


@app.route('/train_algorithm', methods=["POST"])
def train_algorithm():

    # TODO load training data from field
    path_to_data = Path(app.root_path).joinpath("data", "abt.csv")

    if request.form.get("cart_select") is not None:
        # Train cart selection
        x_train, x_test, y_train, y_test = model.get_train_test(path_to_data.as_posix())

        cart_model = CARTAlgorithm(x_train.values, y_train.values, x_test.values, y_test.values, request.form.get("cart_criterion"))
        cart_model.build_model()
        prediction = cart_model.get_predictions(x_test.values)

        scores = cart_model.get_statistical_metrics()

        # print("The prediction accuracy is: ", cart_model.score(test_features, test_targets) * 100, "%")
        a = 5






