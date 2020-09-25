NEXT_MEAL_TIME_DIFFERENCE = 3

# Celery Tasks Names
DAILY_WEIGHT_ASSESSMENTS = "check_and_create_daily_weight_assessment"
PENDING_MEAL_PROGRESS = "change_pending_to_progress_daily_weight_assessment_meal"
UPCOMING_MEAL = "send_upcoming_meal_notification"
WEEKLY_WEIGHT_ASSESSMENT = "send_weekly_weight_assessment_notification"
ONE_MONTH_WEIGHT_REASSESSMENT = "send_one_month_reassessment_notification"

# Notification Texts
UPCOMING_MEAL_NOTIFICATION_TEXT = "Remember to eat"
UPCOMING_MEAL_NOTIFICATION_MESSAGE = "You have a meal scheduled at {}"

WEEKLY_CHECK_UP_NOTIFICATION_TEXT = "Weekly Check-up"
WEEKLY_CHECK_UP_NOTIFICATION_MESSAGE = "Log your weight and waist circumference so we can update your progress"
