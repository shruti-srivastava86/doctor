from doctor import enums

WEIGHT = 0
FOOD_AND_HYDRATION = 1
MOTION = 2
SLEEP = 3
MIND = 4

FOR_ASSESSMENT = [
    (WEIGHT, 'Weight'),
    (FOOD_AND_HYDRATION, 'Food and Hydration'),
    (MOTION, 'Motion'),
    (SLEEP, 'Sleep'),
    (MIND, 'Mind'),
]


CANNOT_DO_IT = 4
REMIND_ME_LATER = 5

ASSESSMENT_STATUS = enums.ASSESSMENT_STATUS + [
    (CANNOT_DO_IT, 'Cannot Do It'),
    (REMIND_ME_LATER, 'Remind Me Later')
]
