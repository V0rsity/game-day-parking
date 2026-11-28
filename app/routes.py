# File containing flask routes "/", "/addCourse", "/removeCourse"

from flask import Blueprint, render_template, redirect, session, request, flash
from datetime import datetime, timedelta
from app.games import get_weekday_home_games
from app.courses import add_course, remove_course
from app.conflicts import add_conflicts

GAMES_CACHE_MINUTES = 10 # Games do not change frequently, so 10 minutes is a reliable cache time

main_blueprint = Blueprint("main", __name__)

# The route that returns the main page.
@main_blueprint.route("/")
def main_page():
    # Cache the games fetched from ESPN for 10 minutes. Without this, the app had to pull from ESPN after every add/remove course
    # Skipping this repetitive API call greatly reduces page load time
    # Reduces the API requests from ESPN so less chance of rate limiting
    last_game_fetch_time = session.get("games_fetch_time")
    games = session.get("games")
    now = datetime.now()
    if (not games) or (not last_game_fetch_time) or (now - timedelta(minutes=GAMES_CACHE_MINUTES) > datetime.fromisoformat(last_game_fetch_time)):
        games = get_weekday_home_games()
        session["games"] = games
        session["games_fetch_time"] = now.isoformat()

    courses = session.get("courses") or []
    add_conflicts(games, courses)
    return render_template("index.html", games=games, courses=courses)

@main_blueprint.route("/addCourse", methods=["POST"])
def add_user_course():
    courses = session.get("courses") or []

    # Get the course inputs from html form
    course_name = request.form.get("course_name")
    is_on_monday = request.form.get("is_on_monday")
    is_on_tuesday = request.form.get("is_on_tuesday")
    is_on_wednesday = request.form.get("is_on_wednesday")
    is_on_thursday = request.form.get("is_on_thursday")
    is_on_friday = request.form.get("is_on_friday")
    course_start = request.form.get("course_start")
    course_end = request.form.get("course_end")

    course_days = []
    days_string = ""
    if is_on_monday:
        course_days.append("Monday")
        days_string += "M"
    if is_on_tuesday:
        course_days.append("Tuesday")
        days_string += "T"
    if is_on_wednesday:
        course_days.append("Wednesday")
        days_string += "W"
    if is_on_thursday:
        course_days.append("Thursday")
        days_string += "R"
    if is_on_friday:
        course_days.append("Friday")
        days_string += "F"

    try:
        start_time = datetime.strptime(course_start, "%H:%M")
        end_time = datetime.strptime(course_end, "%H:%M")
    except:
        flash(message="Failed to add course: Time could not be parsed")
        return redirect("/")
    
    new_course = {
        "name" : course_name,
        "days" : course_days,
        "displayDays" : days_string,
        "startTime" : start_time.strftime("%H:%M"),
        "endTime" : end_time.strftime("%H:%M"),
        "displayStartTime" : start_time.strftime("%I:%M %p"),
        "displayEndTime" : end_time.strftime("%I:%M %p")
    }

    result = add_course(courses, new_course)

    if result[0]:
        session["courses"] = result[1]  # Set the "courses" session value to the new array with the course added
        return redirect("/")

    else:
        flash(message=("Failed to add course: " + result[1]))  # Flash stores error in session to be shown on main page
        return redirect("/")

@main_blueprint.route("/removeCourse/<course_name>", methods=["POST"])
def remove_user_course(course_name):
    courses = session.get("courses") or []
    result = remove_course(courses, course_name)
    if result[0]:
        session["courses"] = result[1]
        return redirect("/")

    else:
        flash(message=("Failed to remove course: " + result[1]))
        return redirect("/")
