"""Helpers for getting and analyzing words."""

import os
import pandas as pd


DIRNAME = os.path.dirname(__file__)
DATA_PATH = os.path.join(DIRNAME, os.pardir, 'data-general')

def get_ousiometry_path() -> os.path:
    return os.path.join(DATA_PATH, 'ousiometer', 'ousiometry_data.txt')
