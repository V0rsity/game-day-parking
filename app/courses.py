# Recieves courses array and attempts to add the course to the array
    # Can be added: Returns True and the new courses array
    # Cannot be added: Returns False and an error message detailing why course cannot be added
def add_course(courses, new_course):
    for c in courses:
        # Names must be unique, necessary for removing them
        if new_course["name"] == c["name"]:
            return (False, "Failed to add course: course name already exists")
        # Ensure that the times do not conflict on each day the course occurs
        for day in new_course["days"]:
            if day in c["days"]:
                if (new_course["startTime"] < c["endTime"] and c["startTime"] < new_course["endTime"]):
                    return (False, "Failed to add course: time conflicts with existing course")
    # Create and return new updated array
    new_courses = courses + [new_course]
    return (True, new_courses)
