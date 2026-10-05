from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Profile


class StudentAuthenticationTests(TestCase):
    def test_signup_creates_user_with_hashed_password_and_profile(self):
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username": "student1",
                "full_name": "Student One",
                "phone": "1234567890",
                "password1": "SafePassword!234",
                "password2": "SafePassword!234",
            },
        )

        self.assertRedirects(response, reverse("accounts:dashboard"))
        user = get_user_model().objects.get(username="student1")
        self.assertTrue(user.check_password("SafePassword!234"))
        self.assertNotEqual(user.password, "SafePassword!234")
        self.assertEqual(user.profile.full_name, "Student One")
        self.assertEqual(user.profile.phone, "1234567890")
        self.assertEqual(user.profile.college_name, "")
        self.assertEqual(user.profile.college_id, "")

    def test_signup_rejects_mismatched_passwords(self):
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username": "student1",
                "full_name": "Student One",
                "phone": "",
                "password1": "SafePassword!234",
                "password2": "DifferentPassword!234",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(get_user_model().objects.filter(username="student1").exists())

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("accounts:dashboard"))

        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={reverse('accounts:dashboard')}",
        )

    def test_login_and_logout(self):
        user = get_user_model().objects.create_user(
            username="student1",
            password="SafePassword!234",
        )
        Profile.objects.create(
            user=user,
            full_name="Student One",
            phone="",
            college_name="",
            college_id="",
        )

        response = self.client.post(
            reverse("accounts:login"),
            {"username": "student1", "password": "SafePassword!234"},
        )
        self.assertRedirects(response, reverse("accounts:dashboard"))
        self.assertIn("_auth_user_id", self.client.session)

        response = self.client.post(reverse("accounts:logout"))
        self.assertRedirects(response, reverse("home"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_navigation_changes_for_authenticated_users(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, reverse("accounts:signup"))
        self.assertContains(response, reverse("accounts:login"))

        user = get_user_model().objects.create_user(
            username="student1",
            password="SafePassword!234",
        )
        self.client.force_login(user)
        response = self.client.get(reverse("home"))
        self.assertContains(response, reverse("accounts:dashboard"))
        self.assertContains(response, reverse("accounts:logout"))
        self.assertNotContains(response, reverse("accounts:signup"))
