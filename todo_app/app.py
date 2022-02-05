from flask import Flask, render_template, request, redirect, url_for
from todo_app.data.trello_items import get_items, add_item, item_in_progress, item_completed, reset_item_status

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())

@app.route('/')
def index():
    """
    Returns the list of saved todo items.
    """
    items = get_items()
    return render_template("index.html", items=items)

@app.route('/item', methods = ['POST'])
def add_new_item():
    """
    Returns the list of saved todo items from Trello web app. Redirects the user back to the index page

    """
    if request.method == "POST":
        new_item = request.form.get("title")
        add_item(new_item)
        return redirect(url_for('index'))
    else:
        return render_template("index.html")

@app.route('/complete', methods = ['POST', 'GET'])
def set_item_to_complete():
    """
    Marks an item as completed. Redirects the user back to the index page

    """
    if request.method == "POST":
        completed_item = request.form.get("mark as completed")
        item_completed(completed_item)
        return redirect(url_for('index'))
    else:
        return render_template("index.html")

@app.route('/inprogress', methods = ['POST', 'GET'])
def set_item_to_progress():
    """
    Sets an item as in progresss. Redirects the user back to the index page

    """
    if request.method == "POST":
        in_progress = request.form.get("set to progress")
        item_in_progress(in_progress)
        return redirect(url_for('index'))
    else:
        return render_template("index.html")

@app.route('/reset', methods = ['POST', 'GET'])
def set_item_status():
    """
    Resets an item status.

    """
    if request.method == "POST":
        reset_item = request.form.get("Reset item status")
        reset_item_status(reset_item)
        return redirect(url_for('index'))
    else:
        return render_template("index.html")


