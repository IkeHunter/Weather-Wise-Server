import environ
import json
from logic.models import Page, Conditions, Forecast, ForecastTable, ForecastRow

env = environ.Env()
environ.Env.read_env()

class Archive:
    def __init__(self):
        pass

    def _fetch_all_days(self):
        pass

    def get_all_days(self):
        pass

    def register_results(self, results: json):
        pass

