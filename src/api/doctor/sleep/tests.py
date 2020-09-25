from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from doctor import enums
from doctor.sleep import enums as sleep_enums
from doctor.sleep.factory import SleepAssessmentFactory
from doctor.sleep.models import SleepDailyAssessment
from doctor.sleep.tasks import task_check_and_create_daily_sleep_assessment
from doctor.user.tests import (
    UserSetup,
    UserTestUtils
)


class SleepTestUtils(object):

    @staticmethod
    def get_sleep_daily_assessment_retrieve_url():
        return reverse('doctor.sleep:assessment')

    @staticmethod
    def get_sleep_daily_assessment_log_url(id):
        return reverse('doctor.sleep:daily_assessment', kwargs={"pk": id})

    @staticmethod
    def get_sleep_overview_url():
        return reverse('doctor.sleep:overview')


class SleepAssessmentRetrieveViewTest(UserSetup):

    def test_sleep_daily_assessment_retrieve_view(self):
        response = self.user_client.get(
            SleepTestUtils.get_sleep_daily_assessment_retrieve_url()
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get('sleep_hours_each_night'),
            SleepAssessmentFactory.sleep_hours_each_night
        )


class SleepDailyAssessmentLogViewTest(UserSetup):
    data = {
        "total_completed": 8,
        "sleep_type": sleep_enums.HEALTHY
    }

    def test_sleep_daily_assessment_log_retrieve_view(self):
        response = self.user_client.get(
            UserTestUtils.get_user_dashboard_url()
        )
        sleep_assessment = response.data.get('sleep')
        if sleep_assessment:
            response = self.user_client.patch(
                SleepTestUtils.get_sleep_daily_assessment_log_url(
                    response.data.get('sleep').get('id')
                ),
                data=self.data
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('status'), enums.COMPLETE)

    def test_sleep_daily_assessment_log_view(self):
        response = self.user_client.get(
            UserTestUtils.get_user_dashboard_url()
        )
        sleep_assessment = response.data.get('sleep')
        if sleep_assessment:
            response = self.user_client.patch(
                SleepTestUtils.get_sleep_daily_assessment_log_url(
                    response.data.get('sleep').get('id')
                ),
                data=self.data
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            dashboard_response = self.user_client.get(
                UserTestUtils.get_user_dashboard_url()
            )
            dashboard_response_sleep_assessment = dashboard_response.data.get('sleep')
            self.assertEqual(
                dashboard_response_sleep_assessment.get('total_completed'),
                self.data.get('total_completed')
            )


class SleepCheckCreateAssessmentTest(UserSetup):
    data = {
        "total_completed": 6,
        "assessment_date": (timezone.now() - timedelta(days=1)).date(),
        "sleep_type": sleep_enums.HEALTHY
    }

    def test_task_check_and_create_daily_sleep_assessment(self):
        dashboard_response = self.user_client.get(
            UserTestUtils.get_user_dashboard_url()
        )
        sleep_assessment = dashboard_response.data.get('sleep')
        if sleep_assessment:
            sleep_assessment = SleepDailyAssessment.objects.get(
                id=dashboard_response.data.get('sleep').get('id')
            )
            sleep_assessment.assessment_date = (timezone.now() - timedelta(days=1)).date()
            sleep_assessment.save()
            task_check_and_create_daily_sleep_assessment(test=True)
            response = self.user_client.get(
                SleepTestUtils.get_sleep_daily_assessment_log_url(
                    dashboard_response.data.get('sleep').get('id')
                )
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            sleep_assessment = SleepDailyAssessment.objects.get(
                id=dashboard_response.data.get('sleep').get('id')
            )
            self.assertEqual(sleep_assessment.status, enums.INCOMPLETE)


class SleepOverviewViewTest(UserSetup):

    def test_sleep_overview(self):
        response = self.user_client.get(
            SleepTestUtils.get_sleep_overview_url()
        )
        self.assertContains(response, "status")
