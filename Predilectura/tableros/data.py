"""Prepare data for Plotly Dash."""
import numpy as np
import pandas as pd

from Predilectura import mongo

def create_dataframe():
    """Create Pandas DataFrame from mongodb."""
    # Load DataFrame
    data = list(mongo.db.abt.find())
    df = pd.DataFrame(list(data))
    df['_id'] = df['_id'].astype(str)
    df['avg_percent'] = pd.to_numeric(df['avg_percent'], errors='coerce')
    df['min_percent'] = pd.to_numeric(df['min_percent'], errors='coerce')
    df['max_percent'] = pd.to_numeric(df['max_percent'], errors='coerce')
    df['avg_words'] = pd.to_numeric(df['avg_words'], errors='coerce')
    df['max_words'] = pd.to_numeric(df['max_words'], errors='coerce')
    df['min_words'] = pd.to_numeric(df['min_words'], errors='coerce')
    return df
