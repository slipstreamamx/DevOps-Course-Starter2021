from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, login_user, UserMixin
from todo_app.data.trello_items import get_items, add_item, item_in_progress, item_completed, reset_item_status
from todo_app.data.user_login import get_user_identity_endpoint, get_user_data_endpoint, get_access_token_endpoint
import os

from todo_app.flask_config import Config
from todo_app.view_model import ViewModel

app.config['LOGIN_DISABLED'] = os.getenv('LOGIN_DISABLED') == 'True'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())  

    login_manager = LoginManager()

    @login_manager.unauthorized_handler
    def unauthenticated():
        return redirect(get_user_identity_endpoint())
        

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    login_manager.init_app(app)

    @app.route('/login/callback', methods=['GET'])
    def login_callback():
        args = request.args
        request_token = args.get('code')
        access_token = get_access_token_endpoint(request_token)

        user_data = get_user_data_endpoint(access_token)

        login_user(User(user_data['id']))

        return redirect(url_for('index'))

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