from services.data_processing.feature_ranking import FeatureRanking
from services.data_processing.exploration import DataExploration
from data.global_variables import GlobalVariables
import pandas as pd

import os.path as path
from pathlib import Path


class Cache:
    feature_ranking = 0
    exploration = 0
    filled = False

    @staticmethod
    def fill_cache():
        if not Cache.filled:
            Cache.feature_ranking = FeatureRanking.feature_ranking(
                pd.read_csv(path.join(Path(__file__).resolve().parents[0], "data", r"data.csv"), dtype=str),
                [
                    GlobalVariables.DatasetColumns.numerical_continuous,
                    GlobalVariables.DatasetColumns.numerical_discrete,
                    GlobalVariables.DatasetColumns.categorical,
                    GlobalVariables.DatasetColumns.binary,
                    GlobalVariables.DatasetColumns.text
                 ],
                GlobalVariables.DatasetColumns.class_label
            )
            #Cache.exploration = DataExploration.explore(pd.read_csv(path.join(Path(__file__).resolve().parents[0], "data", r"data.csv"), dtype=str))
            Cache.filled = True
