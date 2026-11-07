# `pip install pytest` to install pytest
# `pytest games_tests.py` to run tests

from app.games import get_weekday_home_games
from datetime import datetime

games = get_weekday_home_games()

def testThereAreGames():
    assert len(games) > 0

def testGamesAreNotOnWeekends():
    for game in games:
        assert not(game["dayOfWeek"] == "Sunday" or game["dayOfWeek"] == "Sunday")

def testGamesHaveProperType():
    for game in games:
        assert (game["type"] == "W" or game["type"] == "M")

def testAwayTeamNotPurdue():
    for game in games:
        assert (game["team"] != "Purdue")

def testDayOfWeekCorrect():
    for game in games:
        date_time = datetime.fromisoformat(game["dateTime"])
        assert (date_time.strftime("%A") == game["dayOfWeek"])

def testDateTimeIsoEST():
    for game in games:
        assert game["dateTime"][-6:] == "-05:00"

def testTimeMatchesDateTime():
    for game in games:
        date_time = datetime.fromisoformat(game["dateTime"])
        assert (date_time.strftime("%H:%M") == game["time"])

def testGamesInChronologicalOrder():
    for i in range(1, len(games)):
        assert games[i-1]["dateTime"] < games[i]["dateTime"]
