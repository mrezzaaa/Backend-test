from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad Request", "message": str(error)}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not Found", "message": str(error)}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred"}), 500
    


#This code defines a function register_error_handlers that registers custom error handlers for a Flask application.
#The function takes a Flask app instance as an argument and defines three error handlers for HTTP error codes 400, 404, and 500.
#Each error handler returns a JSON response with a corresponding error message and the original error code.
#This function is likely called in the application initialization code, passing the Flask app instance as an argument, to register these error handlers.