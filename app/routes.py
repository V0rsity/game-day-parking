# File containing flask routes "/", "/addCourse", "/removeCourse"

from flask import Blueprint, render_template
from app.games import get_weekday_home_games

main_blueprint = Blueprint("main", __name__)

# The route that returns the main page.
@main_blueprint.route("/")
def main_page():
    games = get_weekday_home_games()
    return render_template("index.html", games=games)
