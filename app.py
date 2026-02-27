import os
import datetime
import logging
import redis
import utilities
import exceptions as AppCustomExceptions
from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
from src.dsa.routes import dsa_bp
from src.misc.routes import misc_bp
from src.auth.google.routes import auth_bp

from json import JSONEncoder
# logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logger.level = logging.DEBUG

# app
app = Flask(__name__)
app.config.from_object('setup.config.Config')

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)
# Assign the custom encoder to the app
app.json_encoder = CustomJSONEncoder

# credentials key value
app.config["CREDENTIALS_SESSION_KEY"] = utilities.CredentialsKey()

# redis configuration
redis_connection = redis.from_url(app.config["REDIS_CONN_STRING"])
utilities.check_redis_connection(
    redis_connection, 
    on_exception_raise=AppCustomExceptions.RedisConnectionFailed,
    logger=logger
)
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis_connection
Session(app)

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health')
def health():
    return {"healthy": True}

@app.route('/ankit-loves-shalu')
def message_1():
    return render_template('shalu.html')

@app.route('/callback', methods=['POST'])
def push_notification_webhook():
    print('-'*15)
    print('API Called')
    print(request.headers)
    print('-'*15)
    return {}

@app.route('/api/auth/status', methods=['GET'])
def api_auth_status():
    """
    API endpoint to check authentication status and retrieve user information.
    
    Returns JSON with:
    - authenticated: boolean indicating if user is logged in
    - name: user's full name (if authenticated)
    - email: user's email (if authenticated)
    - profile_picture: user's profile picture URL (if authenticated and available)
    """
    
    # Check if user is authenticated
    is_authenticated = utilities.is_authenticated()
    
    response = {
        'authenticated': is_authenticated
    }
    
    if is_authenticated:
        # Get user info from session
        id_info = session.get('id_info', {})
        
        # Extract user information
        response['name'] = id_info.get('name', 'User')
        response['email'] = id_info.get('email', '')
        
        # Get profile picture from Google
        profile_picture = id_info.get('picture', None)
        response['profile_picture'] = profile_picture
    
    return jsonify(response)

# Route Registration
app.register_blueprint(dsa_bp, url_prefix='/dsa')
app.register_blueprint(auth_bp, url_prefix='/auth')

# Register misc route only in debug mode
if app.debug:
    app.register_blueprint(misc_bp, url_prefix='/misc')


# if __name__ != '__main__':
#     # Get the gunicorn error logger
#     gunicorn_logger = logging.getLogger('gunicorn.error')
#     # Assign gunicorn's handlers and level to your app's logger
#     app.logger.handlers = gunicorn_logger.handlers
#     app.logger.setLevel(gunicorn_logger.level)

if __name__ == '__main__':

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = {True: '1', False: '0'}[app.config['GOOGLE_INSECURE_MODE']]
    app.run(host='0.0.0.0', port=app.config["PORT"])
