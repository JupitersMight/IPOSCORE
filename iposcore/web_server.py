import os
from flask import Flask, render_template, send_from_directory
from services.data_processing.feature_ranking import FeatureRanking
from services.data_processing.exploration import DataExploration
from data.global_variables import GlobalVariables
import pandas as pd

import os.path as path
from pathlib import Path

app = Flask(__name__,
            template_folder='templates',
            static_url_path='',
            static_folder='public'
            )


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'public'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/feature_ranking')
def feature_ranking():
    data = pd.read_csv(path.join(Path(__file__).resolve().parents[0], 'data', r'data.csv'), dtype=str)
    feature_ranking = FeatureRanking.feature_ranking(
        data,
        [
            GlobalVariables.DatasetColumns.numerical_continuous,
            GlobalVariables.DatasetColumns.numerical_discrete,
            GlobalVariables.DatasetColumns.categorical,
            GlobalVariables.DatasetColumns.binary,
            GlobalVariables.DatasetColumns.text
         ],
        GlobalVariables.DatasetColumns.class_label
    )

    return render_template("feature_ranking.html", data=feature_ranking)

@app.route('/exploration')
def exploration():
    data = pd.read_csv(path.join(Path(__file__).resolve().parents[0], 'data', r'data.csv'), dtype=str)
    exploration = DataExploration.explore(data)

    return render_template('exploration.html', data=exploration)

@app.route('/')
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)

