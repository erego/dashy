"""Prepare data for Plotly Dash."""
from pathlib import Path
import glob
import numpy as np
import pandas as pd
import json

from flask import current_app as app

from Predilectura import mongo

def create_dataframe():
    """Create Pandas DataFrame from csv."""
    # Load DataFrame
    path_to_data = Path(app.root_path).joinpath("data", "abt.csv")

    data = pd.read_csv(path_to_data.as_posix())
    return data

def get_datasets():
    """Get list of datasets used"""
    lst_datasets = list(Path(app.root_path).joinpath("data").glob('*.csv'))
    lst_datasets = [dataset.name for dataset in lst_datasets]
    return lst_datasets


def get_json_algorithm(algorithm, dataset):
    file_json = f'{dataset.split(".csv")[0]}_{algorithm}.json'
    path_to_json = Path(app.root_path).joinpath("model", file_json)

    with open(path_to_json) as f:
        data = json.load(f)

    return data

