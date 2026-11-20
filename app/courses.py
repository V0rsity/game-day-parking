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

# Recieves courses array and attempts to remove course by inputted name
    # If removed successfully: Returns True with updated array
    # If failed to remove: Returns False with error message
def remove_course(courses, course_name):
    for c in courses:
        if course_name == c["name"]: # Find existing record with name, add_course() should ensure no duplicates
            # Create and return new list
            new_courses = list(courses)
            new_courses.remove(c)
            return (True, new_courses)
    return (False, "Failed to remove course: name not found")
