from doctor.badges import enums
from doctor.food_hydration.models import (
    FoodAndHydrationDailyAssessment,
    FoodAndHydrationDaysRange
)
from doctor.mind.models import (
    MindDailyAssessment,
    MindDaysRange
)
from doctor.motion.models import (
    MotionDailyAssessment,
    MotionDaysRange
)
from doctor.sleep.models import (
    SleepDailyAssessment,
    SleepDaysRange
)
from doctor.surrounding.models import (
    SurroundingDailyAssessment,
    SurroundingDaysRange
)
from doctor.weight.models import (
    WeightDailyAssessment,
    WeightDaysRange
)


MAXIMUM_INITIAL_ASSESSMENT_SCORE = 33
TOTAL_INSTALLATION_DAYS = 66
TOTAL_INITIAL_ASSESSMENT_SCORE = 50
TOTAL_INSTALLATION_SCORE = 50
TOTAL_SCORE = 100

SUCCESS_NOTIFICATION_MESSAGE = "Successfully ran {} task"
FAILED_NOTIFICATION_MESSAGE = "Failed to run {} task with error: {}"
FAILED_NOTIFICATION_USER_MESSAGE = "Failed to run {} task for user {} with error: {}"


#########################
#  Notification Texts   #
#########################
CHECK_TASK_NOTIFICATION_TEXT = "Good Morning"
CHECK_TASK_NOTIFICATION_MESSAGE = "Remember to check your Daily Habits and Alerts for today!"

INCOMPLETE_CHECK_TASK_NOTIFICATION_TEXT = "Complete your day"
INCOMPLETE_CHECK_TASK_NOTIFICATION_MESSAGE = "Remember to update your habit trackers before the end of Today!"

WEIGHT_ASSESSMENT_INSTALLED_TEXT = "Congratulations!"
WEIGHT_ASSESSMENT_INSTALLED_MESSAGE = "You've installed a healthy habit from Weight Management"

FOOD_AND_HYDRATION_ASSESSMENT_INSTALLED_TEXT = "Well Done!"
FOOD_AND_HYDRATION_ASSESSMENT_INSTALLED_MESSAGE = "You've installed a healthy habit from Food & Hydration"

MOTION_ASSESSMENT_INSTALLED_TEXT = "Super!"
MOTION_ASSESSMENT_INSTALLED_MESSAGE = "You've installed a healthy habit from Motion"

SLEEP_ASSESSMENT_INSTALLED_TEXT = "Perfect!"
SLEEP_ASSESSMENT_INSTALLED_MESSAGE = "You've installed a healthy habit from Sleep"

MIND_ASSESSMENT_INSTALLED_TEXT = "Great Work!"
MIND_ASSESSMENT_INSTALLED_MESSAGE = "You've installed a healthy habit from Mind"

SURROUNDING_ASSESSMENT_INSTALLED_TEXT = "Completed it!"
SURROUNDING_ASSESSMENT_INSTALLED_MESSAGE = "You've completed all of the Surrounding's tasks"

INCOMPLETE_ASSESSMENT_NOTIFICATION_TEXT = "You Failed a Day!"
INCOMPLETE_ASSESSMENT_NOTIFICATION_MESSAGE = "You didn't complete your habit tracking for {} yesterday"

INCOMPLETE_ASSESSMENT_DAY_NOTIFICATION_TEXT = "You Failed {} days in a row!"
INCOMPLETE_ASSESSMENT_DAY_NOTIFICATION_MESSAGE = "You've failed to track your daily habit in {} for {} days now"

HABIT_NOTIFICATION_TEXT = {
    enums.WEIGHT: {
        "text": WEIGHT_ASSESSMENT_INSTALLED_TEXT,
        "message": WEIGHT_ASSESSMENT_INSTALLED_MESSAGE
    },
    enums.FOOD_AND_HYDRATION: {
        "text": FOOD_AND_HYDRATION_ASSESSMENT_INSTALLED_TEXT,
        "message": FOOD_AND_HYDRATION_ASSESSMENT_INSTALLED_MESSAGE
    },
    enums.MOTION: {
        "text": MOTION_ASSESSMENT_INSTALLED_TEXT,
        "message": MOTION_ASSESSMENT_INSTALLED_MESSAGE
    },
    enums.SLEEP: {
        "text": SLEEP_ASSESSMENT_INSTALLED_TEXT,
        "message": SLEEP_ASSESSMENT_INSTALLED_MESSAGE
    },
    enums.MIND: {
        "text": MIND_ASSESSMENT_INSTALLED_TEXT,
        "message": MIND_ASSESSMENT_INSTALLED_MESSAGE
    },
    enums.SURROUNDINGS: {
        "text": SURROUNDING_ASSESSMENT_INSTALLED_TEXT,
        "message": SURROUNDING_ASSESSMENT_INSTALLED_MESSAGE
    }
}


###############################
#  Reassessment Alert Texts   #
###############################
WEEKLY_REASSESSMENT_ALERT_TEXT = "{} week check-up"
WEEKLY_REASSESSMENT_ALERT_MESSAGE = "Tap to check-in and see if you're still keeping on top of {}"
WEEKLY_REASSESSMENT_ALERT_MIND_MESSAGE = "Tap to check-in and see if you're still working on having a healthy Mind"

MONTHLY_REASSESSMENT_ALERT_TEXT = "{} month check-up"
MONTHLY_REASSESSMENT_ALERT_MESSAGE = "Let's check if you're still keeping on top of {}"
MONTHLY_REASSESSMENT_ALERT_MIND_MESSAGE = "Let’s check if you’re still working on having a healthy Mind"


#########################
#   Celery Task Names   #
#########################
TASKS_CHECK = "send_check_tasks_for_the_day_notification"
INCOMPLETE_TASKS_CHECK = "send_incomplete_check_tasks_for_the_day_notification"
HABIT_INSTALLING_TASK = "task_send_assessment_installed_notification"
WEEKLY_ASSESSMENT_TASK = "task_send_weekly_reassessment_alert"
MONTHLY_ASSESSMENT_TASK = "task_send_monthly_reassessment_alert"


#########################
#    Celery Run Time    #
#########################
CRON_30_MINUTES = '*/30'

TASK_CHECK_REMINDER_TIME_HOUR = 7
TASK_CHECK_REMINDER_TIME_MINUTE = 30

INCOMPLETE_TASK_CHECK_REMINDER_TIME_HOUR = 20
INCOMPLETE_TASK_CHECK_REMINDER_TIME_MINUTE = 00

WEEKLY_REMINDER_TIME_HOUR = 7
WEEKLY_REMINDER_TIME_MINUTE = 30


###############################
#    Assessment Dictionary    #
###############################
ASSESSMENT_DAYS_RANGE_CATEGORY_BY_TYPE = {
    enums.WEIGHT: {
        "assessment": WeightDailyAssessment,
        "days_range": WeightDaysRange,
        "category": "Weight Management"
    },
    enums.FOOD_AND_HYDRATION: {
        "assessment": FoodAndHydrationDailyAssessment,
        "days_range": FoodAndHydrationDaysRange,
        "category": "Food and Hydration"
    },
    enums.MOTION: {
        "assessment": MotionDailyAssessment,
        "days_range": MotionDaysRange,
        "category": "Motion"
    },
    enums.SLEEP: {
        "assessment": SleepDailyAssessment,
        "days_range": SleepDaysRange,
        "category": "Sleep"
    },
    enums.MIND: {
        "assessment": MindDailyAssessment,
        "days_range": MindDaysRange,
        "category": "Mind"
    },
    enums.SURROUNDINGS: {
        "assessment": SurroundingDailyAssessment,
        "days_range": SurroundingDaysRange,
        "category": "Surrounding"
    }
}
