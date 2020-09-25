from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from doctor.food_hydration.factory import FoodAndHydrationAssessmentFactory
from doctor.food_hydration.tasks import task_check_and_create_daily_food_and_hydration_assessment
from doctor.user.tests import (
    UserSetup,
    UserTestUtils
)
from doctor import enums


class FoodAndHydrationTestUtils(object):

    @staticmethod
    def get_food_and_hydration_daily_assessment_retrieve_url():
        return reverse('doctor.food_hydration:assessment')

    @staticmethod
    def get_food_and_hydration_daily_assessment_log_url(id):
        return reverse('doctor.food_hydration:daily_assessment', kwargs={"pk": id})

    @staticmethod
    def get_food_and_hydration_overview_url():
        return reverse('doctor.food_hydration:overview')


class FoodAndHydrationAssessmentRetrieveViewTest(UserSetup):

    def test_food_and_hydration_daily_assessment_retrieve_view(self):
        response = self.user_client.get(
            FoodAndHydrationTestUtils.get_food_and_hydration_daily_assessment_retrieve_url()
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get('glasses_of_water_per_day'),
            FoodAndHydrationAssessmentFactory.glasses_of_water_per_day
        )


class FoodAndHydrationDailyAssessmentLogViewTest(UserSetup):
    data = {
        "total_completed": 2
    }

    def test_food_and_hydration_daily_assessment_log_retrieve_view(self):
        response = self.user_client.get(
            UserTestUtils.get_user_dashboard_url()
        )
        food_and_hydration_assessment = response.data.get('food_hydration')
        if food_and_hydration_assessment:
            response = self.user_client.get(
                FoodAndHydrationTestUtils.get_food_and_hydration_daily_assessment_log_url(
                    response.data.get('food_hydration').get('id')
                )
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_food_and_hydration_daily_assessment_log_view(self):
        response = self.user_client.get(
            UserTestUtils.get_user_dashboard_url()
        )
        food_and_hydration_assessment = response.data.get('food_hydration')
        if food_and_hydration_assessment:
            response = self.user_client.patch(
                FoodAndHydrationTestUtils.get_food_and_hydration_daily_assessment_log_url(
                    response.data.get('food_hydration').get('id')
                ),
                data=self.data
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            dashboard_response = self.user_client.get(
                UserTestUtils.get_user_dashboard_url()
            )
            dashboard_response_food_and_hydration_assessment = dashboard_response.data.get('food_hydration')
            self.assertEqual(
                dashboard_response_food_and_hydration_assessment.get('total_completed'),
                self.data.get('total_completed')
            )


class FoodAndHydrationCheckCreateAssessmentTest(UserSetup):
    data = {
        "assessment_date": (timezone.now() - timedelta(days=1)).date()
    }

    def test_task_check_and_create_daily_food_and_hydration_assessment(self):
        dashboard_response = self.user_client.get(
            UserTestUtils.get_user_dashboard_url()
        )
        food_and_hydration_assessment = dashboard_response.data.get('food_hydration')
        if food_and_hydration_assessment:
            update_response = self.user_client.patch(
                FoodAndHydrationTestUtils.get_food_and_hydration_daily_assessment_log_url(
                    dashboard_response.data.get('food_hydration').get('id')
                ),
                data=self.data
            )
            self.assertEqual(update_response.status_code, status.HTTP_200_OK)
            self.assertEqual(update_response.data.get('status'), enums.IN_PROGRESS)
            task_check_and_create_daily_food_and_hydration_assessment(test=True)
            response = self.user_client.get(
                FoodAndHydrationTestUtils.get_food_and_hydration_daily_assessment_log_url(
                    dashboard_response.data.get('food_hydration').get('id')
                )
            )
            self.assertEqual(response.data.get('status'), enums.INCOMPLETE)


class FoodAndHydrationOverviewViewTest(UserSetup):

    def test_food_and_hydration_overview(self):
        response = self.user_client.get(
            FoodAndHydrationTestUtils.get_food_and_hydration_overview_url()
        )
        self.assertContains(response, "status")
