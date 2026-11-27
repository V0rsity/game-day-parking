# File containing code to identify game-day course conflicts

# Note: There is no explicit guideline for what time Purdue Parking will choose to close lots.
#       Everything here is based on my personal experience as a Purdue commuter to Ross Ade and may be subject to change

from datetime import datetime, timedelta

LATEST = "17:00"  # Latest I have seen a tow time this year (5:00)
LIKELY_BUFFER_HOURS = 2  # Hours before game time that the tow time is typically in effect
POTENTIAL_BUFFER_HOURS = 2.5  # A potential extra buffer for big games that start at 7, I could see lots potentially closing at 4:30
GAME_TIME_HOURS = 2.5  # Accounts for if there is somehow a class after the game is over. I doubt they would tow after the game

def add_conflicts(games, courses):
    for game in games:
        # Determine when the game will be over and people can park again
        game_end_time = datetime.strftime(
            datetime.strptime(game["time"], "%H:%M") + timedelta(hours=GAME_TIME_HOURS), "%H:%M"
        )
        # Determine the time when it is likely the lot will close
        likely_buffer_time = datetime.strftime(
            datetime.strptime(game["time"], "%H:%M") - timedelta(hours=LIKELY_BUFFER_HOURS), "%H:%M"
        )
        # Determine the earliest a lot would likely close
        possible_buffer_time = datetime.strftime(
            datetime.strptime(game["time"], "%H:%M") - timedelta(hours=POTENTIAL_BUFFER_HOURS), "%H:%M"
        )

        conflicts = []  
        for course in courses:
            # No conflict if game is already over
            if course["startTime"] >= game_end_time:
                continue

            if game["dayOfWeek"] in course["days"]:
                # If the course end is after the latest I have seen tow time, it is very likely to conflict with tow time
                if course["endTime"] >= LATEST:
                    conflicts.append({
                        "course" : course["name"],
                        "startTime" : course["displayStartTime"],
                        "endTime" : course["displayEndTime"],
                        "conflictLevel" : "Very Likely",
                        "conflictColor" : "#FF000095"
                    })
                    continue

                # If the course end falls in the likely buffer, drivers should consider planning to move their car
                if course["endTime"] >= likely_buffer_time:
                    conflicts.append({
                        "course" : course["name"],
                        "startTime" : course["displayStartTime"],
                        "endTime" : course["displayEndTime"],
                        "conflictLevel" : "Likely",
                        "conflictColor" : "#FFA50095"
                    })

                # If the course falls in the possible buffer time, the likelihood of conflicting with tow time is a toss-up
                elif course["endTime"] >= possible_buffer_time:
                    conflicts.append({
                        "course" : course["name"],
                        "startTime" : course["displayStartTime"],
                        "endTime" : course["displayEndTime"],
                        "conflictLevel" : "Possible",
                        "conflictColor" : "#FFFF0095"
                    })

        game["conflicts"] = conflicts
