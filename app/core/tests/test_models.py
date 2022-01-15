from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """TEST IF USER MEETS OUR EMAIL OR PASSWORD WE SET"""

        email = "mur@test.com"
        password = "mur123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))



    def test_new_user_email_normalized(self):
        """TESTING IF THE WRITTEN EMAIL IS WELL NORMALIZED AT DOMAIN PART"""

        email = 'mur@TEST.COM'
        user = get_user_model().objects.create_user(email, 'mur123')

        self.assertEqual(user.email, email.lower())


    def test_new_user_invalid_email(self):
        """TEST IF A NEW USER HAS TYPED EMAIL"""
        with self.assertRaises(ValueError):
         get_user_model().objects.create_user(None, 'test123')


    def test_create_new_superuser(self):
        """TEST CREATING A NEW SUPERUSER"""
        user= get_user_model().objects.create_superuser(
            'mur@test.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
