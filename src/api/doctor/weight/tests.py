from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from doctor.user.tests import UserSetup, UserTestUtils
from doctor.weight import enums
from doctor.weight.factory import WeightAssessmentFactory
from doctor.weight.tasks import (
    task_check_and_create_daily_weight_assessment,
    task_change_pending_to_progress_weight_assessment_meal
)


class WeightTestUtils(object):

    @staticmethod
    def get_weight_assessment_retrieve_update_url():
        return reverse('doctor.weight:assessment')

    @staticmethod
    def get_weight_daily_assessment_log_url(id):
        return reverse('doctor.weight:daily_assessment', kwargs={"pk": id})

    @staticmethod
    def get_weight_overview_url():
        return reverse('doctor.weight:overview')


class WeightDailyAssessmentLogViewTest(UserSetup):
    data = {
        "first_meal_of_day": timezone.now().strftime("%H:%M"),
        "meal_plan": enums.FIVE_AND_ONE
    }
    meal_data = {
        "meal": {
            "meal_type": 2,
            "status": 1
        }
    }
    assessment_data = {
        "assessment_date": (timezone.now() - timedelta(days=1)).date()
    }

    def test_weight_daily_assessment_retrieve_view(self):
        response = self.user_client.get(
            WeightTestUtils.get_weight_assessment_retrieve_update_url()
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get('bmi'),
            WeightAssessmentFactory.bmi
        )

    def test_weight_assessment_update_view(self):
        response = self.user_client.patch(
            WeightTestUtils.get_weight_assessment_retrieve_update_url(),
            data=self.data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.user.weight_assessment.first_meal_of_day.strftime('%H:%M'),
            self.data["first_meal_of_day"]
        )
        self.assertEqual(
            self.user.weight_assessment.meal_plan,
            self.data["meal_plan"]
        )

    def test_weight_daily_assessment_log_retrieve_view(self):
        response = self.user_client.get(
            UserTestUtils.get_user_dashboard_url()
        )
        weight_assessment = response.data.get('weight')
        if weight_assessment:
            response = self.user_client.get(
                WeightTestUtils.get_weight_daily_assessment_log_url(
                    response.data.get('weight').get('id')
                )
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_weight_daily_assessment_log_view(self, **kwargs):
        self.test_weight_assessment_update_view()
        task_change_pending_to_progress_weight_assessment_meal(test=True)
        response = self.user_client.get(
            UserTestUtils.get_user_dashboard_url()
        )
        assessment_meals = response.data.get('weight').get('meals')
        progress_assessment_meal = [
            assessment_meal['id'] for assessment_meal in assessment_meals
            if (
                   assessment_meal['status'] == enums.IN_PROGRESS
               ) or (
                assessment_meal['status'] == enums.PENDING
            )
        ]
        if progress_assessment_meal:
            self.meal_data["meal"]["id"] = progress_assessment_meal[0]
            if kwargs.get('assessment_date'):
                self.meal_data['assessment_date'] = kwargs.get('assessment_date')
            response = self.user_client.patch(
                WeightTestUtils.get_weight_daily_assessment_log_url(
                    response.data.get('weight').get('id')
                ),
                data=self.meal_data,
                format='json'
            )
            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK
            )
            self.assertEqual(
                response.data['meals'][0]['status'],
                self.meal_data['meal']['status']
            )

    def test_task_check_and_create_daily_weight_assessment(self):
        self.test_weight_daily_assessment_log_view(
            assessment_date=self.assessment_data.get('assessment_date')
        )
        task_check_and_create_daily_weight_assessment(test=True)
        response = self.user_client.get(
            UserTestUtils.get_user_dashboard_url()
        )
        self.assertEqual(response.data.get('weight', None), None)


class WeightOverviewViewTest(UserSetup):

    def test_weight_overview(self):
        response = self.user_client.get(
            WeightTestUtils.get_weight_overview_url()
        )
        self.assertContains(response, "status")
