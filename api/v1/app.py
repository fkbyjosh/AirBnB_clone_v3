#!/usr/bin/python3
""" 
Flask Application for AirBnB clone REST API
Includes Swagger documentation, CORS support, and error handling
"""
from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from

# Initialize Flask application
app = Flask(__name__)

# Configure application
app.config.update(
    JSONIFY_PRETTYPRINT_REGULAR=True,
    SWAGGER={
        'title': 'AirBnB clone Restful API',
        'uiversion': 3
    }
)

# Register blueprints
app.register_blueprint(app_views)

# Setup CORS
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def close_db(error):
    """ 
    Close Storage connection after each request
    Args:
        error: Possible error to handle
    """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """ 
    Handle 404 errors
    Args:
        error: Error to handle
    Returns:
        JSON response with 404 status code
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)

# Initialize Swagger documentation
swagger = Swagger(app)

if __name__ == '__main__':
    """
    Main Flask application entry point
    """
    # Get host and port from environment or use defaults
    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    port = environ.get('HBNB_API_PORT', 5000)
    
    # Run application
    app.run(host=host, port=port, threaded=True)
