from flask import Blueprint, render_template

web_bp = Blueprint("web", __name__)

@web_bp.route("/")
def home():
    """Renders the single-page research application."""
    return render_template("index.html")
