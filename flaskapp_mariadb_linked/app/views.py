from flask import render_template
from app import app, db
from .models import Testmariadb

@app.route('/')
@app.route('/index')
def index():
    title = "Flask App"
    paragraph = ["Simple app to query a Database in Docker."]
    users = Testmariadb.query.all()
    return render_template("index.html", title=title, paragraph=paragraph, users=users)
