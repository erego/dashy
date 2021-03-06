"""Routes for parent Flask app."""

import pickle
import json

from pathlib import Path

from flask import current_app as app
from flask import render_template, request, g, redirect, url_for

from Predilectura.statistics.dataset_abt import DataSetABT
from Predilectura.statistics.abt import ABTPandas

import pandas as pd

from Predilectura import mongo, babel
from Predilectura.statistics.abt import ABTMongoDB, ABTPandas
from Predilectura.statistics.feature import Feature, FeatureContinuous, FeatureCategorical
from Predilectura.mlearning.information_based import CARTAlgorithm, C4dot5Algorithm, RandomForestAlgorithm, \
    GradientBoostingAlgorithm
from Predilectura.mlearning.similarity_based import KNearestNeighboursAlgorithm, KMeansAlgorithm
from Predilectura.mlearning.probability_based import NaiveBayesAlgorithm
from Predilectura.mlearning.multilayer_perceptron_based import PerceptronsAlgorithm
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
        title="Visualization Data",
        description="Embed Plotly Dash into your Flask applications.",
        template="home-template",
        body="This is a homepage served with Flask.",
    )


@app.route("/datos")
# TODO uncomment login_required
# @login_required
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

    path_to_events = Path(app.root_path).joinpath("data", "../data/events.csv")
    events = pd.read_csv(path_to_events.as_posix())

    total_records = len(events.index)
    number_of_records = 10
    total_pages = int(total_records / 10) + 1
    current_page = int(request.args.get('page', default=1))
    number_to_skip = number_of_records * (current_page - 2)
    if current_page == 1:
        data = pd.read_csv(path_to_events.as_posix(), nrows=number_of_records)
    else:
        data = pd.read_csv(path_to_events.as_posix(), skiprows=range(number_to_skip + 1,
                                                                     number_to_skip + number_of_records + 1),
                           nrows=number_of_records)
    data = data.copy().T.to_dict().values()
    return render_template('lista_events.jinja2', events=data, prev=current_page - 1, current=current_page,
                           next=current_page + 1, total_pages=total_pages)


@app.route("/listar_readings")
def lista_readings():
    """
    Page which list reading collection
    """

    path_to_readings = Path(app.root_path).joinpath("data", "../data/readings.csv")
    readings = pd.read_csv(path_to_readings.as_posix())

    total_records = len(readings.index)

    number_of_records = 10
    total_pages = int(total_records / 10) + 1
    current_page = int(request.args.get('page', default=1))
    number_to_skip = number_of_records * (current_page - 2)

    if current_page == 1:
        data = pd.read_csv(path_to_readings.as_posix(), nrows=number_of_records)
    else:
        data = pd.read_csv(path_to_readings.as_posix(), skiprows=range(number_to_skip + 1,
                                                                       number_to_skip + number_of_records + 1),
                           nrows=number_of_records)
    data = data.copy().T.to_dict().values()

    return render_template('lista_readings.jinja2', readings=data, prev=current_page - 1, current=current_page,
                           next=current_page + 1, total_pages=total_pages)


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
        number_to_skip = number_of_records * (current_page - 1)

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

    return render_template('lista_abt.jinja2', abt=data, prev=current_page - 1, current=current_page,
                           next=current_page + 1, total_pages=total_pages, header=dict_header, format_data=format_data)


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
    dict_abt_features["min_time_session"] = True if request.form.get("min_time_session") is not None else False
    dict_abt_features["max_time_session"] = True if request.form.get("max_time_session") is not None else False
    dict_abt_features["avg_time_session"] = True if request.form.get("avg_time_session") is not None else False
    dict_abt_features["time_last_session"] = True if request.form.get("time_last_session") is not None else False

    output_ath = request.form.get("output_path")
    path_to_data = Path(app.root_path).joinpath("data", output_ath)
    if request.form.get("output_format") == "pandas":
        abt_to_create = ABTPandas(dict_abt_features, path_to_data)
        abt_to_create.create_ABT()
    elif request.form.get("output_format") == "mongodb":
        abt_to_create = ABTMongoDB(dict_abt_features, path_to_data)
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

    form.abts.choices = [(element, element) for element in ABTPandas.get_list_abt()]

    path_to_data = Path(app.root_path).joinpath("data", "abt.csv")

    columns = pd.read_csv(path_to_data.as_posix(), index_col=0, nrows=0).columns.tolist()

    form.features_select.choices = [(column, column) for column in columns]

    return render_template('gestion_calidad_abt.jinja2', form=form)


@app.route("/handle_quality_issues", methods=["POST"])
def handle_quality_issues():
    selected_option = request.form.get("handler")
    lst_features = request.form.getlist("features_select")
    path_to_data = Path(app.root_path).joinpath("data", request.form.get("abts"))
    if request.form.get("filename", None) is not None:
        path_to_output = Path(app.root_path).joinpath("data", request.form.get("filename"))
    else:
        path_to_output = path_to_data

    dataset_abt = DataSetABT(path_to_data.as_posix())
    if selected_option == "drop_features":
        dataset_abt.drop_features(lst_features, path_to_output.as_posix())
    elif selected_option == "missing_reading":
        dataset_abt.missing_reading_indicator(path_to_output.as_posix())
    elif selected_option == "complete_case":
        dataset_abt.complete_case_analysis(path_to_output.as_posix())
    elif selected_option == "imputation":
        dataset_abt.imputation(lst_features, request.form.get("imputation"), path_to_output.as_posix())
    elif selected_option == "clamp":
        dataset_abt.clamp(lst_features, path_to_output.as_posix())

    return redirect(url_for('quality_abt', format_data="pandas"))
    return render_template('lista_datos.jinja2')


@app.route('/algorithm_train')
def algorithm_train():
    form = FormAlgorithm()
    form.abts.choices = [(element, element) for element in ABTPandas.get_list_abt()]

    return render_template('algorithm_train.jinja2', form=form)


@app.route('/train_algorithm', methods=["POST"])
def train_algorithm():

    path_to_data = Path(app.root_path).joinpath("data", request.form.get("abts"))
    filename_noextension = path_to_data.stem
    path_to_model_folder = Path(app.root_path).joinpath("model")
    path_to_model_folder.mkdir(parents=True, exist_ok=True)
    x_train, x_test, y_train, y_test = model.get_train_test(path_to_data.as_posix())

    if request.form.get("cart_select") is not None:
        # Train cart selection
        cart_model = CARTAlgorithm(x_train.values, y_train.values, x_test.values, y_test.values,
                                   request.form.get("cart_criterion"))
        cart_model.build_model()

        lst_features = list(x_train.columns)
        cart_model.export_tree(lst_features)

        file_model = f'{filename_noextension}_CART.pkl'
        path_to_model = path_to_model_folder.joinpath(file_model)
        file_metrics = f'{filename_noextension}_CART.json'
        path_to_metrics = path_to_model_folder.joinpath(file_metrics)

        with open(path_to_model, 'wb') as f:
            pickle.dump(cart_model, f)

        scores = cart_model.get_statistical_metrics()

        with open(path_to_metrics, 'w') as fp:
            json.dump(scores, fp)

    if request.form.get("random_forest_select") is not None:
        # Train random forest selection
        random_forest_model = RandomForestAlgorithm(x_train.values, y_train.values, x_test.values, y_test.values)
        random_forest_model.build_model()

        lst_features = list(x_train.columns)
        random_forest_model.export_tree(lst_features)

        file_model = f'{filename_noextension}_RF.pkl'
        path_to_model = path_to_model_folder.joinpath(file_model)
        file_metrics = f'{filename_noextension}_RF.json'
        path_to_metrics = path_to_model_folder.joinpath(file_metrics)

        with open(path_to_model, 'wb') as f:
            pickle.dump(random_forest_model, f)

        scores = random_forest_model.get_statistical_metrics()

        with open(path_to_metrics, 'w') as fp:
            json.dump(scores, fp)

    if request.form.get("xgboost_select") is not None:
        # Train gradient boosting selection

        lst_features = list(x_train.columns)
        lst_features.append("target")
        print(lst_features)
        xgboost_model = GradientBoostingAlgorithm(x_train.values, y_train.values, x_test.values, y_test.values, lst_features)
        xgboost_model.build_model()

        xgboost_model.export_tree()
        file_model = f'{filename_noextension}_GB.pkl'
        path_to_model = path_to_model_folder.joinpath(file_model)
        file_metrics = f'{filename_noextension}_GB.json'
        path_to_metrics = path_to_model_folder.joinpath(file_metrics)

        with open(path_to_model, 'wb') as f:
            pickle.dump(xgboost_model, f)

        scores = xgboost_model.get_statistical_metrics()

        with open(path_to_metrics, 'w') as fp:
            json.dump(scores, fp)

    if request.form.get("c4dot5_select") is not None:
        # Train c4.5 selection

        c4dot5_model = C4dot5Algorithm(x_train, y_train, x_test, y_test)
        c4dot5_model.build_model()

        file_model = f'{filename_noextension}_C4dot5.pkl'
        path_to_model = path_to_model_folder.joinpath(file_model)
        file_metrics = f'{filename_noextension}_C4dot5.json'
        path_to_metrics = path_to_model_folder.joinpath(file_metrics)

        c4dot5_model.save_model(path_to_model.as_posix())

        scores = c4dot5_model.get_statistical_metrics()

        with open(path_to_metrics, 'w') as fp:
            json.dump(scores, fp)

    if request.form.get("knearestneighbours_select") is not None:
        # Train KNN selection
        knn_model = KNearestNeighboursAlgorithm(x_train.values, y_train.values, x_test.values, y_test.values,
                                                request.form.get("knearestneighbours_weights"))
        knn_model.build_model()
        file_model = f'{filename_noextension}_KNN.pkl'
        path_to_model = path_to_model_folder.joinpath(file_model)
        file_metrics = f'{filename_noextension}_KNN.json'
        path_to_metrics = path_to_model_folder.joinpath(file_metrics)

        with open(path_to_model, 'wb') as f:
            pickle.dump(knn_model, f)

        scores = knn_model.get_statistical_metrics()

        with open(path_to_metrics, 'w') as fp:
            json.dump(scores, fp)

    if request.form.get("kmeans_select") is not None:
        # Train Kmeans selection
        kmeans_model = KMeansAlgorithm(x_train.values, y_train.values, x_test.values, y_test.values,
                                       request.form.get("kmeans_algorithm"))
        kmeans_model.build_model()
        file_model = f'{filename_noextension}_kmeans.pkl'
        path_to_model = path_to_model_folder.joinpath(file_model)
        file_metrics = f'{filename_noextension}_kmeans.json'
        path_to_metrics = path_to_model_folder.joinpath(file_metrics)

        with open(path_to_model, 'wb') as f:
            pickle.dump(kmeans_model, f)

        scores = kmeans_model.get_statistical_metrics()

        with open(path_to_metrics, 'w') as fp:
            json.dump(scores, fp)

    if request.form.get("naivebayes_select") is not None:
        # Train naive bayes selection
        naivebayes_model = NaiveBayesAlgorithm(x_train.values, y_train.values, x_test.values, y_test.values)
        naivebayes_model.build_model()
        file_model = f'{filename_noextension}_naivebayes.pkl'
        path_to_model = path_to_model_folder.joinpath(file_model)
        file_metrics = f'{filename_noextension}_naivebayes.json'
        path_to_metrics = path_to_model_folder.joinpath(file_metrics)

        with open(path_to_model, 'wb') as f:
            pickle.dump(naivebayes_model, f)

        scores = naivebayes_model.get_statistical_metrics()

        with open(path_to_metrics, 'w') as fp:
            json.dump(scores, fp)

    if request.form.get("mlp_select") is not None:
        # Train multilayer perceptron selection
        mlp_model = PerceptronsAlgorithm(x_train.values, y_train.values, x_test.values, y_test.values)
        mlp_model.build_model()
        file_model = f'{filename_noextension}_mlp.pkl'
        path_to_model = path_to_model_folder.joinpath(file_model)
        file_metrics = f'{filename_noextension}_mlp.json'
        path_to_metrics = path_to_model_folder.joinpath(file_metrics)

        with open(path_to_model, 'wb') as f:
            pickle.dump(mlp_model, f)

        scores = mlp_model.get_statistical_metrics()

        with open(path_to_metrics, 'w') as fp:
            json.dump(scores, fp)

    return render_template('lista_datos.jinja2')
