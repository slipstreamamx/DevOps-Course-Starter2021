from flask import Flask, render_template, request, redirect, url_for
from todo_app.data.trello_items import get_items, add_item, in_progress

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())

@app.route('/')
def index():
    """
    Returns the list of saved todo items and sorts by status in descending order. Sorts the item list by status ("Not Started", then "Completed")

    """
    items = get_items()
    # sorted_items = sorted(items, key=lambda item: item["status"], reverse=True)
    return render_template("index.html", items=items)

@app.route('/item', methods = ['POST'])
def add_task():
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
def complete_task():
    """
    Marks an item as completed. Redirects the user back to the index page

    """
    if request.method == "POST":
        completed_item = request.form.get("mark complete")
        update_item = get_item(completed_item)
        update_item["status"] = "Completed"
        save_item(update_item)
        return redirect(url_for('index'))
    else:
        return render_template("index.html")

@app.route('/inprogress', methods = ['POST', 'GET'])
def task_inprogress():
    """
    Sets an item as in progresss. Redirects the user back to the index page

    """
    if request.method == "POST":
        item_in_progress = request.form.get("set to progress")
        in_progress(item_in_progress)
        # update_item["status"] = "In Progress"
        # save_item(update_item)
        return redirect(url_for('index'))
    else:
        return render_template("index.html")

@app.route('/remove', methods = ['POST', 'GET'])
def delete_task():
    """
    Removes an item from the session using new funtion called delete_item from session_items.

    """
    if request.method == "POST":
        remove_item = request.form.get("delete item")
        update_item = get_item(remove_item)
        delete_item(update_item)
        return redirect(url_for('index'))
    else:
        return render_template("index.html")


