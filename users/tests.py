from django.http import response
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username": 'rizo_17o7',
                "first_name": 'muhammad',
                "last_name": 'botirov',
                "email": 'botirovmuhammadrizo61@gmail.com',
                "password": 'somepassword',
            }
        )

        user = get(username='rizo_17o7')

        self.assertEqual(user.first_name, "muhammad")
        self.assertEqual(user.last_name, "botirov")
        self.assertEqual(user.email, "botirovmuhammadrizo61@gmail.com")
        self.assertNotEqual(user.password, "somepassword")
        self.assertTrue(user.check_password("somepassword"))

    def test_invalid_email(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username": 'rizo_17o7',
                "first_name": 'muhammad',
                "last_name": 'botirov',
                "email": 'botirovmuhammadrizo61@gmail.com',
                "password": 'somepassword',
            }
        )
        user_count = User.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')








