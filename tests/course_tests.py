# `pip install pytest` to install pytest
# `pytest course_tests.py` to run tests, must be in /tests

from app.courses import add_course, remove_course

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
    {
        "name" : "CS193",
        "days" : ["Tuesday"],
        "startTime" : "12:30",
        "endTime" : "13:20",
        "displayStartTime" : "12:30 PM",
        "displayEndTime" : "1:20 PM",
    },
]

def testAddValidCourse():
    new_course = {
        "name" : "Accounting",
        "days" : ["Monday", "Wednesday", "Friday"],
        "startTime" : "09:30",
        "endTime" : "10:20",
        "displayStartTime" : "09:30 AM",
        "displayEndTime" : "10:20 AM",
    }
    result = add_course(courses, new_course)
    assert result[0]
    assert new_course in result[1]

def testAddInvalidCourse():
    new_course = {
        "name" : "Accounting",
        "days" : ["Monday", "Tuesday", "Friday"],
        "startTime" : "15:30",
        "endTime" : "16:20",
        "displayStartTime" : "3:30 PM",
        "displayEndTime" : "4:20 PM",
    }
    result = add_course(courses, new_course)
    assert not result[0]

def testConflictingTimeValidDay():
    new_course = {
        "name" : "Accounting",
        "days" : ["Tuesday", "Thursday"],
        "startTime" : "15:30",
        "endTime" : "16:20",
        "displayStartTime" : "3:30 PM",
        "displayEndTime" : "4:20 PM",
    }
    result = add_course(courses, new_course)
    assert result[0]
    assert new_course in result[1]

def testSameName():
    new_course = {
        "name" : "CS180",
        "days" : ["Thursday"],
        "startTime" : "15:30",
        "endTime" : "16:20",
        "displayStartTime" : "03:30 PM",
        "displayEndTime" : "04:20 PM",
    }
    result = add_course(courses, new_course)
    assert not result[0]

def testBlankCourses():
    new_course = {
        "name" : "CS180",
        "days" : ["Thursday"],
        "startTime" : "15:30",
        "endTime" : "16:20",
        "displayStartTime" : "03:30 PM",
        "displayEndTime" : "04:20 PM",
    }
    result = add_course([], new_course)
    assert result[0]
    assert new_course in result[1]

def testNewCourseBlank():
    new_course = {
        "name" : "",
        "days" : ["Thursday"],
        "startTime" : "15:30",
        "endTime" : "16:20",
        "displayStartTime" : "03:30 PM",
        "displayEndTime" : "04:20 PM",
    }
    result = add_course(courses, new_course)
    assert not result[0]

def testNewCourseDaysEmpty():
    new_course = {
        "name" : "Soc",
        "days" : [],
        "startTime" : "15:30",
        "endTime" : "16:20",
        "displayStartTime" : "03:30 PM",
        "displayEndTime" : "04:20 PM",
    }
    result = add_course(courses, new_course)
    assert not result[0]

def testNewCourseTimeNone():
    new_course = {
        "name" : "Soc",
        "days" : ["Wednesday"],
        "startTime" : None,
        "endTime" : "16:20",
        "displayStartTime" : None,
        "displayEndTime" : "04:20 PM",
    }
    result = add_course(courses, new_course)
    assert not result[0]

def testNewCourseStartAfterEnd():
    new_course = {
        "name" : "Soc",
        "days" : ["Wednesday"],
        "startTime" : "17:30",
        "endTime" : "16:20",
        "displayStartTime" : "5:30 PM",
        "displayEndTime" : "04:20 PM",
    }
    result = add_course(courses, new_course)
    assert not result[0]

def testNewCourseStartEqualsEnd():
    new_course = {
        "name" : "Soc",
        "days" : ["Wednesday"],
        "startTime" : "16:20",
        "endTime" : "16:20",
        "displayStartTime" : "04:20 PM",
        "displayEndTime" : "04:20 PM",
    }
    result = add_course(courses, new_course)
    assert not result[0]

def testRemoveCourseExists():
    result = remove_course(courses, "CS180")
    assert result[0]
    assert len(result[1]) == 2
    assert len(courses) == 3 # remove_course should not change the original list

def testRemoveCourseDoesNotExist():
    result = remove_course(courses, "Soc")
    assert not result[0]

def testRemoveCourseEmptyArray():
    result = remove_course([], "CS180")
    assert not result[0]
