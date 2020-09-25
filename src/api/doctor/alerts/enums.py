GENERAL = 0
TODAY = 1
COMPLETED = 2
REMINDER = 3
FAILED = 4
BADGE = 5
WEEKLY_WEIGHT_CHECKUP = 6
ONE_WEEK_CHECKUP = 7
TWO_WEEK_CHECKUP = 8
THREE_WEEK_CHECKUP = 9
ONE_MONTH_CHECKUP = 10
TWO_MONTH_CHECKUP = 11

ALERT_TYPE = (
    (GENERAL, 'General'),
    (TODAY, 'Today'),
    (REMINDER, 'Reminder'),
    (COMPLETED, 'Completed'),
    (FAILED, 'Failed'),
    (BADGE, 'Badge'),
    (WEEKLY_WEIGHT_CHECKUP, 'Weekly Weight Checkup'),
    (ONE_WEEK_CHECKUP, 'One Week Checkup'),
    (TWO_WEEK_CHECKUP, 'Two Week Checkup'),
    (THREE_WEEK_CHECKUP, 'Three Week Checkup'),
    (ONE_MONTH_CHECKUP, 'One Month Checkup'),
    (TWO_MONTH_CHECKUP, 'Two Month Checkup')
)

WEIGHT = 0
FOOD_AND_HYDRATION = 1
MOTION = 2
SLEEP = 3
MIND = 4
SURROUNDING = 5

MACRO_TYPE = (
    (WEIGHT, 'Weight'),
    (FOOD_AND_HYDRATION, 'Food and Hydration'),
    (MOTION, 'Motion'),
    (SLEEP, 'Sleep'),
    (MIND, 'Mind'),
    (SURROUNDING, 'Surrounding')
)

WELCOME = 0
MISSING_A_DAY = 1
FAILING_A_MACRO = 2
STOP_CHALLENGE_CHOOSE = 3
WEIGHT_INSTALLATION = 4
FOOD_AND_HYDRATION_INSTALLATION = 5
MOTION_INSTALLATION = 4
SLEEP_INSTALLATION = 5
MIND_INSTALLATION = 6

VIDEO_TYPES = (
    (WELCOME, 'Welcome'),
    (MISSING_A_DAY, 'Missing a Day'),
    (FAILING_A_MACRO, 'Failing a Macro'),
    (STOP_CHALLENGE_CHOOSE, 'Stop Challenge Choose'),
    (WEIGHT_INSTALLATION, 'Weight Installation'),
    (FOOD_AND_HYDRATION_INSTALLATION, 'Food and Hydration Installation'),
    (MOTION_INSTALLATION, 'Motion Installation'),
    (SLEEP_INSTALLATION, 'Sleep Installation'),
    (MIND_INSTALLATION, 'Mind Installation')
)
