"""Generic enum fields"""
IN_PROGRESS = 0
COMPLETE = 1
INCOMPLETE = 2
RESET = 3
LOCKED = 4

ASSESSMENT_STATUS = [
    (IN_PROGRESS, 'In Progress'),
    (COMPLETE, 'Complete'),
    (INCOMPLETE, 'Incomplete'),
    (RESET, 'Reset')
]
