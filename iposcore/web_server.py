import os
from flask import Flask, render_template, send_from_directory
from cache import Cache

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
    return render_template("feature_ranking.html", data=Cache.feature_ranking)

@app.route('/exploration')
def exploration():
    return render_template('exploration.html', data=Cache.exploration)

@app.route('/')
def home():
    return render_template("home.html")


if __name__ == "__main__":
    Cache.fill_cache()
    app.run()

