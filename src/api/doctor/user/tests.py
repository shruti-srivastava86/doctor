from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from doctor.food_hydration.factory import (
    FoodAndHydrationDaysRangeFactory
)
from doctor.mind.factory import MindDaysRangeFactory
from doctor.motion.factory import MotionDaysRangeFactory
from doctor.sleep.factory import SleepDaysRangeFactory
from doctor.surrounding.factory import SurroundingDaysRangeFactory
from doctor.user.factory import UserFactory
from doctor.weight.factory import WeightDaysRangeFactory


class UserSetup(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user_client = APIClient()
        self.user_client.force_authenticate(user=self.user)


class UserTestUtils(object):

    @staticmethod
    def get_user_signup_url():
        return reverse('doctor.user:sign_up')

    @staticmethod
    def get_user_login_url():
        return reverse('doctor.user:login')

    @staticmethod
    def get_user_logout_url():
        return reverse('doctor.user:logout')

    @staticmethod
    def get_user_profile_url():
        return reverse('doctor.user:profile')

    @staticmethod
    def get_user_forgot_password_url(email):
        return reverse('doctor.user:forgot_password_email')

    @staticmethod
    def get_user_change_password_url():
        return reverse('doctor.user:change_password')

    @staticmethod
    def get_user_dashboard_url():
        return reverse('doctor.user:dashboard')

    @staticmethod
    def get_user_results_url():
        return reverse('doctor.user:results')

    @staticmethod
    def get_user_notification_settings_url():
        return reverse('doctor.user:notification_settings')


class UserSignupTest(APITestCase):
    data = {
        "name": "Shruti Srivastava",
        "email": "shruti_srivastav86@yahoo.com",
        "password": "Password123",
        "height": 168,
        "waist": 75,
        "weight": 75,
        "dob": "1986-11-26",
        "gender": 0,
        "bmi": 27,
        "glasses_of_water_per_day": 3,
        "average_stress_level": 5,
        "steps_each_day": 3500,
        "sleep_hours_each_night": 6
    }

    def setUp(self):
        WeightDaysRangeFactory()
        FoodAndHydrationDaysRangeFactory()
        MotionDaysRangeFactory()
        SleepDaysRangeFactory()
        MindDaysRangeFactory()
        SurroundingDaysRangeFactory()

    def create_user(self):
        return APIClient().post(
            UserTestUtils.get_user_signup_url(),
            self.data
        )

    def test_user_signup(self):
        response = self.create_user()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.data)
        self.assertTrue('user' in response.data)


class UserLoginTest(APITestCase):
    data = {
        "email": "shruti_srivastav86@yahoo.com",
        "password": "Password123"
    }

    def setUp(self):
        self.user = UserFactory()

    def test_user_login(self):
        response = APIClient().post(
            UserTestUtils.get_user_login_url(),
            self.data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.data)
        self.assertTrue('user' in response.data)


class UserProfileTest(UserSetup):

    def test_user_profile(self):
        response = self.user_client.get(
            UserTestUtils.get_user_profile_url()
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('id' in response.data)


class UserProfileUpdateTest(UserSetup):
    data = {
        "email": "shruti_srivastav86+update@yahoo.com",
        "name": "Shruti Srivastava update",
        "dob": "1988-02-22",
    }

    def test_user_update_profile(self):
        response = self.user_client.patch(
            UserTestUtils.get_user_profile_url(),
            self.data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('email'), self.data['email'])
        self.assertEqual(response.data.get('name'), self.data['name'])
        self.assertEqual(response.data.get('dob'), self.data['dob'])


class UserLogoutTest(UserSetup):

    def test_user_logout(self):
        response = self.user_client.delete(
            UserTestUtils.get_user_logout_url(),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserDeleteTest(UserSetup):

    def test_user_delete(self):
        response = self.user_client.delete(
            UserTestUtils.get_user_profile_url(),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserForgotPasswordTest(UserSetup):

    def test_forgot_password(self):
        data = {
            "email": self.user.email
        }
        response = self.user_client.post(
            UserTestUtils.get_user_forgot_password_url(self.user.email),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserChangePasswordTest(UserSetup):
    data = {
        "old_password": "Password123",
        "password": "Password1234"
    }

    def test_change_password(self):
        response = self.user_client.patch(
            UserTestUtils.get_user_change_password_url(),
            self.data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        login_response = self.user_client.post(
            UserTestUtils.get_user_login_url(),
            UserLoginTest.data
        )
        self.assertEqual(login_response.status_code, status.HTTP_400_BAD_REQUEST)


class UserDashboardView(UserSetup):

    def test_user_dashboard(self):
        response = self.user_client.get(
            UserTestUtils.get_user_dashboard_url()
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserResultsView(UserSetup):

    def test_user_results(self):
        response = self.user_client.get(
            UserTestUtils.get_user_results_url()
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('weight_assessment' in response.data)


class UserNotificationSettingsView(UserSetup):
    data = {
        "meal": False,
        "incomplete_day": False,
        "good_morning": False,
        "weekly_checkup": False
    }

    def test_user_notification_settings(self):
        response = self.user_client.get(
            UserTestUtils.get_user_notification_settings_url()
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_notification_settings_update(self):
        response = self.user_client.patch(
            UserTestUtils.get_user_notification_settings_url(),
            self.data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
