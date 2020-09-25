from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from doctor import enums
from doctor.motion.factory import MotionAssessmentFactory
from doctor.motion.tasks import task_check_and_create_daily_motion_assessment
from doctor.user.tests import (
    UserSetup,
    UserTestUtils
)


class MotionTestUtils(object):

    @staticmethod
    def get_motion_daily_assessment_retrieve_url():
        return reverse('doctor.motion:assessment')

    @staticmethod
    def get_motion_daily_assessment_log_url(id):
        return reverse('doctor.motion:daily_assessment', kwargs={"pk": id})

    @staticmethod
    def get_motion_overview_url():
        return reverse('doctor.motion:overview')


class MotionAssessmentRetrieveViewTest(UserSetup):

    def test_food_and_hydration_daily_assessment_retrieve_view(self):
        response = self.user_client.get(
            MotionTestUtils.get_motion_daily_assessment_retrieve_url()
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get('steps_each_day'),
            MotionAssessmentFactory.steps_each_day
        )


class MotionDailyAssessmentLogViewTest(UserSetup):
    data = {
        "total_completed": 3500
    }

    def test_motion_daily_assessment_log_retrieve_view(self):
        response = self.user_client.get(
            UserTestUtils.get_user_dashboard_url()
        )
        motion_assessment = response.data.get('motion')
        if motion_assessment:
            response = self.user_client.get(
                MotionTestUtils.get_motion_daily_assessment_log_url(
                    response.data.get('motion').get('id')
                ),
                data=self.data
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_motion_daily_assessment_log_view(self):
        response = self.user_client.get(
            UserTestUtils.get_user_dashboard_url()
        )
        motion_assessment = response.data.get('motion')
        if motion_assessment:
            response = self.user_client.patch(
                MotionTestUtils.get_motion_daily_assessment_log_url(
                    response.data.get('motion').get('id')
                ),
                data=self.data
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            dashboard_response = self.user_client.get(
                UserTestUtils.get_user_dashboard_url()
            )
            dashboard_response_motion_assessment = dashboard_response.data.get('motion')
            self.assertEqual(
                dashboard_response_motion_assessment.get('total_completed'),
                self.data.get('total_completed')
            )


class MotionCheckCreateAssessmentTest(UserSetup):
    data = {
        "assessment_date": (timezone.now() - timedelta(days=1)).date()
    }

    def test_task_check_and_create_daily_motion_assessment(self):
        dashboard_response = self.user_client.get(
            UserTestUtils.get_user_dashboard_url()
        )
        motion_assessment = dashboard_response.data.get('motion')
        if motion_assessment:
            update_response = self.user_client.patch(
                MotionTestUtils.get_motion_daily_assessment_log_url(
                    dashboard_response.data.get('motion').get('id')
                ),
                data=self.data
            )
            self.assertEqual(update_response.status_code, status.HTTP_200_OK)
            self.assertEqual(update_response.data.get('status'), enums.IN_PROGRESS)
            task_check_and_create_daily_motion_assessment(test=True)
            response = self.user_client.get(
                MotionTestUtils.get_motion_daily_assessment_log_url(
                    dashboard_response.data.get('motion').get('id')
                )
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('status'), enums.INCOMPLETE)


class MotionOverviewViewTest(UserSetup):

    def test_motion_overview(self):
        response = self.user_client.get(
            MotionTestUtils.get_motion_overview_url()
        )
        self.assertContains(response, "status")
