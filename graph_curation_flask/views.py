from flask import render_template

from graph_curation_flask import app


@app.route('/')
def index():
    app.logger.warning('sample message')
    return render_template('index.html')
