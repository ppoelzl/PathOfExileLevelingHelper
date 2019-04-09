from app import app


@app.errorhandler(404)
def not_found_error(error):
    return "This page does not exist", 404


@app.errorhandler(500)
def internal_error(error):
    return "PoB import failed", 500
