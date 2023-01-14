from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_required, login_user, UserMixin, current_user
from todo_app.data.trello_items import get_items, add_item, item_in_progress, item_completed, reset_item_status
from todo_app.data.user_login import UserAccess
import os
from todo_app.flask_config import Config
from todo_app.view_model import ViewModel
from functools import wraps
import string, random
from loggly.handlers import HTTPSHandler
from logging import Formatter
from pythonjsonlogger import jsonlogger


def user_authorised(func):
    """Check if the user role has access"""

    @wraps(func)
    def auth_wrapper(*args, **kwargs):
        if current_user.user_role != "writer":
            return "Forbidden", 403
        return func(*args, **kwargs)
    return auth_wrapper

class User(UserMixin):
    def __init__(self, id):
        self.id = id
    
    @property
    def user_role(self):
        if self.id == "34609286":
            return "writer"
        else:
            return "reader"

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())  
    app.logger.setLevel(app.config['LOG_LEVEL'])

    login_manager = LoginManager()

    @login_manager.unauthorized_handler
    def unauthenticated():
        state_string  = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        session['user-state'] = state_string
        app.logger.info("User is unauthenticated")
        return redirect('https://github.com/login/oauth/authorize?client_id=' + str(os.getenv('CLIENT_ID')) + '&state=' + state_string)
        

    @login_manager.user_loader
    def load_user(user_id):
        app.logger.info(f"User is authenticated and their role is {User(user_id).user_role}, with ID of {user_id}")        
        return User(user_id)

    login_manager.init_app(app)

    if app.config['LOGGLY_TOKEN'] is not None:
        handler = HTTPSHandler(f'https://logs-01.loggly.com/inputs/{app.config["LOGGLY_TOKEN"]}/tag/todo-app')
        handler.setFormatter(jsonlogger.JsonFormatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s"))
        app.logger.addHandler(handler)

    @app.route('/login/callback', methods=['GET'])
    def login_callback():
        args = request.args
        returedState = args.get('state')
        sessionState = session.get('user-state')        
        request_token = args.get('code')
        access_token = UserAccess.get_access_token(request_token)

        user_data = UserAccess.get_user_data(access_token)
        if returedState == sessionState:
            login_user(User(user_data['id']))

        return redirect(url_for('index'))

    @app.route('/')
    @login_required 
    def index():
        allCards = get_items()
        item_view_model = ViewModel(allCards)
        return render_template('index.html', view_model=item_view_model)

    @user_authorised
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
    @user_authorised 
    def set_item_to_progress(item_id):
        item_in_progress(item_id)
        app.logger.info(f'Card %s {item_id} set to in progress')
        return redirect(url_for('index'))

    @app.route('/items/<item_id>/complete')
    @login_required
    @user_authorised    
    def set_item_to_complete(item_id):
        item_completed(item_id)
        app.logger.info(f'Card %s {item_id} is set to completed')        
        return redirect(url_for('index'))

    @app.route('/items/<item_id>/reset')
    @login_required
    @user_authorised    
    def set_item_status(item_id):
        reset_item_status(item_id)
        app.logger.info(f'Card %s {item_id} reset to Not Started')        
        return redirect(url_for('index'))
    
    return app

if __name__ == '__main__':
    create_app().run()