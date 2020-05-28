from django.apps import AppConfig
from joblib import dump, load
import os
import xgboost as xgb


class PredictConfig(AppConfig):
    name = 'predict'
    model = os.getenv('MODEL','lstm_sample')
    dir_path = os.path.dirname(os.path.realpath(__file__))
    ml = load(f'{dir_path}/ml_output/{model}.joblib')
    # feature_names = ml.get_booster().feature_names
    # bst = xgb.Booster({'nthread': 4})
    # bst.load_model(f'{dir_path}/ml_output/{model}.joblib')
    #

