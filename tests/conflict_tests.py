# `pip install pytest` to install pytest
# `pytest course_tests.py` to run tests, must be in /tests directory

from app.conflicts import add_conflicts

def testGameHasVeryLikelyConflict():
    courses = [
        {
            "name" : "CS180",
            "days" : ["Monday", "Wednesday", "Friday"],
            "startTime" : "16:30",
            "endTime" : "17:20",
            "displayStartTime" : "04:30 PM",
            "displayEndTime" : "05:20 PM",
        },
        {
            "name" : "CS Lab",
            "days" : ["Tuesday"],
            "startTime" : "13:30",
            "endTime" : "15:20",
            "displayStartTime" : "01:30 PM",
            "displayEndTime" : "03:20 PM",
        },
    ]
    games = [
        {
            "type" : "M",
            "name" : "TestTeam",
            "dayOfWeek" : "Wednesday",
            "time" : "18:30",
        }
    ]
    add_conflicts(games=games, courses=courses)

    assert len(games[0]["conflicts"]) == 1
    assert games[0]["conflicts"][0]["course"] == "CS180"
    assert games[0]["conflicts"][0]["conflictLevel"] == "Very Likely"

def testGameHasLikelyConflict():
    courses = [
        {
            "name" : "CS180",
            "days" : ["Monday", "Wednesday", "Friday"],
            "startTime" : "15:30",
            "endTime" : "16:45",
            "displayStartTime" : "03:30 PM",
            "displayEndTime" : "04:45 PM",
        },
        {
            "name" : "CS Lab",
            "days" : ["Tuesday"],
            "startTime" : "13:30",
            "endTime" : "15:20",
            "displayStartTime" : "01:30 PM",
            "displayEndTime" : "03:20 PM",
        },
    ]
    games = [
        {
            "type" : "M",
            "name" : "TestTeam",
            "dayOfWeek" : "Wednesday",
            "time" : "18:30",
        }
    ]
    add_conflicts(games=games, courses=courses)

    assert len(games[0]["conflicts"]) == 1
    assert games[0]["conflicts"][0]["course"] == "CS180"
    assert games[0]["conflicts"][0]["conflictLevel"] == "Likely"

def testGameHasPossibleConflict():
    courses = [
        {
            "name" : "CS180",
            "days" : ["Monday", "Wednesday", "Friday"],
            "startTime" : "15:30",
            "endTime" : "16:20",
            "displayStartTime" : "03:30 PM",
            "displayEndTime" : "04:20 PM",
        },
        {
            "name" : "CS Lab",
            "days" : ["Tuesday"],
            "startTime" : "13:30",
            "endTime" : "15:20",
            "displayStartTime" : "01:30 PM",
            "displayEndTime" : "03:20 PM",
        },
    ]
    games = [
        {
            "type" : "M",
            "name" : "TestTeam",
            "dayOfWeek" : "Wednesday",
            "time" : "18:30",
        }
    ]
    add_conflicts(games=games, courses=courses)

    assert len(games[0]["conflicts"]) == 1
    assert games[0]["conflicts"][0]["course"] == "CS180"
    assert games[0]["conflicts"][0]["conflictLevel"] == "Possible"

def testNoConflicts():
    courses = [
        {
            "name" : "CS180",
            "days" : ["Monday", "Wednesday", "Friday"],
            "startTime" : "15:30",
            "endTime" : "16:20",
            "displayStartTime" : "03:30 PM",
            "displayEndTime" : "04:20 PM",
        },
        {
            "name" : "CS Lab",
            "days" : ["Tuesday"],
            "startTime" : "13:30",
            "endTime" : "15:20",
            "displayStartTime" : "01:30 PM",
            "displayEndTime" : "03:20 PM",
        },
    ]
    games = [
        {
            "type" : "M",
            "name" : "TestTeam",
            "dayOfWeek" : "Wednesday",
            "time" : "20:30",
        }
    ]
    add_conflicts(games=games, courses=courses)

    assert not games[0]["conflicts"]

def testTwoConflicts():
    courses = [
        {
            "name" : "CS180 Gold",
            "days" : ["Monday", "Wednesday", "Friday"],
            "startTime" : "15:30",
            "endTime" : "16:20",
            "displayStartTime" : "03:30 PM",
            "displayEndTime" : "04:20 PM",
        },
        {
            "name" : "CS180 Black",
            "days" : ["Monday", "Wednesday", "Friday"],
            "startTime" : "16:30",
            "endTime" : "17:20",
            "displayStartTime" : "04:30 PM",
            "displayEndTime" : "05:20 PM",
        }
    ]
    games = [
        {
            "type" : "M",
            "name" : "TestTeam",
            "dayOfWeek" : "Wednesday",
            "time" : "18:30",
        }
    ]
    add_conflicts(games=games, courses=courses)

    assert len(games[0]["conflicts"]) == 2
    assert games[0]["conflicts"][0]["course"] == "CS180 Gold"
    assert games[0]["conflicts"][0]["conflictLevel"] == "Possible"
    assert games[0]["conflicts"][1]["course"] == "CS180 Black"
    assert games[0]["conflicts"][1]["conflictLevel"] == "Very Likely"

def testNoConflictsBecauseDifferentDay():
    courses = [
        {
            "name" : "CS180",
            "days" : ["Monday", "Wednesday", "Friday"],
            "startTime" : "16:30",
            "endTime" : "17:20",
            "displayStartTime" : "04:30 PM",
            "displayEndTime" : "05:20 PM",
        },
        {
            "name" : "CS Lab",
            "days" : ["Tuesday"],
            "startTime" : "13:30",
            "endTime" : "15:20",
            "displayStartTime" : "01:30 PM",
            "displayEndTime" : "03:20 PM",
        },
    ]
    games = [
        {
            "type" : "M",
            "name" : "TestTeam",
            "dayOfWeek" : "Thursday", # Different day
            "time" : "20:30",
        }
    ]
    add_conflicts(games=games, courses=courses)

    assert not games[0]["conflicts"]

# The requirements for this may change when I learn exactly what the process is for morning/afternoon games
def testMorningGame():
    courses = [
        {
            "name" : "CS180",
            "days" : ["Monday", "Wednesday", "Friday"],
            "startTime" : "15:30",
            "endTime" : "16:45",
            "displayStartTime" : "03:30 PM",
            "displayEndTime" : "04:45 PM",
        },
        {
            "name" : "Calc Recitation",
            "days" : ["Wednesday"],
            "startTime" : "09:30",
            "endTime" : "10:20",
            "displayStartTime" : "09:30 AM",
            "displayEndTime" : "10:20 AM",
        },
        {
            "name" : "CS 193",
            "days" : ["Wednesday"],
            "startTime" : "12:30",
            "endTime" : "13:20",
            "displayStartTime" : "12:30 PM",
            "displayEndTime" : "01:20 PM",
        },
    ]
    games = [
        {
            "type" : "M",
            "name" : "TestTeam",
            "dayOfWeek" : "Wednesday",
            "time" : "11:00",
        }
    ]
    add_conflicts(games=games, courses=courses)

    assert len(games[0]["conflicts"]) == 2
    assert games[0]["conflicts"][0]["course"] == "Calc Recitation"
    assert games[0]["conflicts"][0]["conflictLevel"] == "Likely"
    assert games[0]["conflicts"][1]["course"] == "CS 193"
    assert games[0]["conflicts"][1]["conflictLevel"] == "Likely" # Leaving this at likely for now, not certain what the protocol is

def testNoCourses():
    courses = []
    games = [
        {
            "type" : "M",
            "name" : "TestTeam",
            "dayOfWeek" : "Wednesday",
            "time" : "11:00",
        }
    ]
    add_conflicts(games=games, courses=courses)

    assert not games[0]["conflicts"]
