# File containing flask routes "/", "/addCourse", "/removeCourse"

from flask import Blueprint, render_template, redirect, session, request, flash
from datetime import datetime
from app.games import get_weekday_home_games
from app.courses import add_course, remove_course

main_blueprint = Blueprint("main", __name__)

# The route that returns the main page.
@main_blueprint.route("/")
def main_page():
    courses = session.get("courses") or []
    games = get_weekday_home_games()
    return render_template("index.html", games=games, courses=courses)

@main_blueprint.route("/addCourse", methods=["POST"])
def add_user_course():
    courses = session.get("courses") or []

    # Get the course inputs from html form
    course_name = request.form.get("course_name")
    course_days = request.form.getlist("course_days")
    course_start = request.form.get("course_start")
    course_end = request.form.get("course_end")

    try:
        start_time = datetime.strptime(course_start, "%H:%M")
        end_time = datetime.strptime(course_end, "%H:%M")
    except:
        flash(message="Failed to add course: Time could not be parsed")
        return redirect("/")
    
    new_course = {
        "name" : course_name,
        "days" : course_days,
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
