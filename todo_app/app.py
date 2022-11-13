from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required
import os
from todo_app.data.trello_items import get_items, add_item, item_in_progress, item_completed, reset_item_status

from todo_app.flask_config import Config
from todo_app.view_model import ViewModel

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())  

    login_manager = LoginManager()

    @login_manager.unauthorized_handler
    def unauthenticated():
        return redirect('https://github.com/login/oauth/authorize?client_id=' + (os.getenv("CLIENT_ID")) + '&state=' + (os.getenv("STATE")))

    @login_manager.user_loader
    def load_user(user_id):
        pass # We will return to this later
        return User.get(user_id)

    login_manager.init_app(app)


    @app.route('/')
    @login_required
    def index():
        allCards = get_items()
        item_view_model = ViewModel(allCards)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/items/new', methods=['POST'])
    @login_required
    def add_new_item():
        name = request.form['name']
        desc = request.form["desc text"]
        due = request.form["date"]
        add_item(name, desc, due)
        return redirect(url_for('index'))

    @app.route('/items/<item_id>/in_progress')
    @login_required
    def set_item_to_progress(item_id):
        item_in_progress(item_id)
        return redirect(url_for('index'))

    @app.route('/items/<item_id>/complete')
    @login_required    
    def set_item_to_complete(item_id):
        item_completed(item_id)
        return redirect(url_for('index'))

    @app.route('/items/<item_id>/reset')
    @login_required 
    def set_item_status(item_id):    
        reset_item_status(item_id)
        return redirect(url_for('index'))
    
    return app

if __name__ == '__main__':
    create_app().run()