from flask import Flask, render_template, request, redirect, url_for
from todo_app.data.session_items import get_items, add_item

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = get_items()
    return render_template("index.html", items=items)

@app.route('/item', methods = ['POST', 'GET'])
def add_task():
    if request.method == "POST":
        new_item = request.form.get("title")
        add_item(new_item)
        return redirect(url_for('index'))
    else:
        return render_template("index.html")

