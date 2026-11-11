import requests  # for http requests
from datetime import datetime, time  # for creating datetime objects and getting days of the week
from zoneinfo import ZoneInfo  # for converting dates to Eastern Standard Time

# ESPN API constants
SEASON_YEAR = "2027"  # hardcoded for now, can't just get current year as 2027 season starts in 2026
PURDUE_TEAM_ID = "2509"
WOMENS_LEAGUE_PATH = "womens-college-basketball"
MENS_LEAGUE_PATH = "mens-college-basketball"

# Time constants
TIMEZONE = "America/New_York"

# Fetches mens and womens weekday home games and returns an array of games in chronological order
def get_weekday_home_games():
    womens_games = get_weekday_home_games_from_espn(WOMENS_LEAGUE_PATH, "W")
    mens_games = get_weekday_home_games_from_espn(MENS_LEAGUE_PATH, "M")
    games = []
    while len(womens_games) > 0 and len(mens_games) > 0:
        if (mens_games[0]["dateTime"] < womens_games[0]["dateTime"]):
            games.append(mens_games[0])
            mens_games.pop(0)
        else:
            games.append(womens_games[0])
            womens_games.pop(0)
    # Append any games left over from the one array that is not empty
    for game in mens_games:
        games.append(game)
    for game in womens_games:
        games.append(game)
    return games

# Fetches either men's or women's games from espn api, returns a trimmed array filtered to weekday home games
def get_weekday_home_games_from_espn(league_path, type):
    path = "https://site.api.espn.com/apis/site/v2/sports/basketball/" + league_path + "/teams/" + PURDUE_TEAM_ID + "/schedule"
    query_params = {"season" : SEASON_YEAR, "seasontype" : "2"}
    response = requests.get(path, params=query_params, timeout=5)
    raw_games = response.json()["events"]
    games = []
    beginning_of_today = datetime.combine(datetime.now().date(), time.min).astimezone(ZoneInfo(TIMEZONE)) # timestamp at 12:00 AM
    for game in raw_games:
        if(game["competitions"][0]['competitors'][0]['id'] == PURDUE_TEAM_ID): # If Purdue is first index in "competitors" -> home game
            date_time = datetime.fromisoformat(game["competitions"][0]["date"]).astimezone(ZoneInfo(TIMEZONE)) # Convert to EST
            day_of_week = date_time.strftime("%A")
            # Filter games to on-or-after current date and not on a weekend
            if not(date_time < beginning_of_today or day_of_week == "Saturday" or day_of_week == "Sunday"):
                # All fields used by the app are determined here, raw data must be trimmed because API response is too large to work with
                games.append({
                    "type" : type,  # 'W' for women's game, 'M' for men's game
                    "team" : game["competitions"][0]['competitors'][1]['team']['shortDisplayName'], # The opposing team name
                    "dateTime" : date_time.isoformat(),  # ISO timestamp
                    "dayOfWeek" : day_of_week,  # The day of the week in EST
                    "time" : date_time.strftime("%H:%M"), # Time in military time
                    "displayTime" : date_time.strftime("%I:%M %p"), # Displays time in AM and PM
                    "displayDate" : date_time.strftime("%m/%d") # Display the date without the year
                })
    return games
