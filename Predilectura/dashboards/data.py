"""Prepare data for Plotly Dash."""
from pathlib import Path

import numpy as np
import pandas as pd

from flask import current_app as app

from Predilectura import mongo

def create_dataframe():
    """Create Pandas DataFrame from csv."""
    # Load DataFrame
    path_to_data = Path(app.root_path).joinpath("data", "abt.csv")

    data = pd.read_csv(path_to_data.as_posix())
    return data
