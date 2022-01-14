from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """TEST IF USER MEETS OUR EMAIL OR PASSWORD WE SET"""

        email = "mur@test.com"
        password = "mur123"
        user = get_user_model().object.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
