"""Weight enum fields"""
FIVE_AND_ONE = 0
THREE_AND_THREE = 1
NO_MEAL_PLAN = 2

MEAL_PLAN = [
    (FIVE_AND_ONE, "Five and One"),
    (THREE_AND_THREE, "Three and Three"),
    (NO_MEAL_PLAN, "No Meal Plan"),
]

HEALTHY = 2
OK = 3
UNHEALTHY = 4

MEAL_TYPE = [
    (FIVE_AND_ONE, "Five and One"),
    (THREE_AND_THREE, "Three and Three"),
    (HEALTHY, "Healthy"),
    (OK, "Ok"),
    (UNHEALTHY, "Unhealthy")
]

IN_PROGRESS = 0
COMPLETE = 1
INCOMPLETE = 2
PENDING = 3

MEAL_ASSESSMENT_STATUS = [
    (IN_PROGRESS, 'In Progress'),
    (COMPLETE, 'Complete'),
    (INCOMPLETE, 'Incomplete'),
    (PENDING, 'Pending')
]
