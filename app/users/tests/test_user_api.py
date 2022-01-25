from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('users:create')
TOKEN_URL = reverse('users:token')
# ME_URL = reverse('users:me')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """TEST USERS API (Public) """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """TEST CREATE USER WITH VALID PAYLOAD IS SUCCESSFUL"""
        payload = {
            'email': "test@test.com",
            'password': 'testpass',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """TEST CREATING USER THAT ALREADY EXISTS """
        payload ={
            'email': "test@test.com",
            'password': 'testpass'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """TEST FOR SHORT PASSWORD  DURING POST"""
        payload = {
            'email': "test@test.com",
            'password': 'pw',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """TEST THAT TOKEN IS CREATED FOR THE USER"""
        payload = { 'email': "test@test.com", 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """TEST THAT TOKEN IS NOT CREATED IF INVALID CREDENTIAL ARE GIVEN"""
        create_user(email='test@test.com', password='testpass')
        payload = {'email': "test@test.com", 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """TEST THAT TOKEN IS NOT CREATED IF USER DOES NOT EXIST"""
        payload = {'email': "test@test.com", 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """TEST THAT EMAIL AND PASSWORD ARE REQUIRED"""
        res = self.client.post(TOKEN_URL, {'email': 'test@test.com', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_retrieve_user_unauthenticated(self):
    #     """TEST THAT AUTHENTICATION IS REQUIRED FOR USERS"""
    #     res = self.client.get(ME_URL)
    #     self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

# class PrivateUserAPITests(TestCase):
#     """TEST API REQUESTS THAT REQUIRE AUTHENTICATION"""
#
#     def setup(self):
#         self.user = create_user(
#             email='test@test.com',
#             password='testpass',
#             name='Test Name'
#         )
#         self.client = APIClient()
#         self.client.force_authenticated(user=self.user)
#
#     def test_retrieve_profile_success(self):
#         """TEST RETRIEVING PROFILE FOR LOGGED IN USER"""
#         res = self.client.get(ME_URL)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, {
#             'name': self.user.name,
#             'email': self.user.email
#         })
#
#     def test_post_me_not_allowed(self):
#         """TEST THAT POST IS NOT ALLOWED ON THE ME URL"""
#         res = self.client.post(ME_URL, {})
#
#         self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
#
#     def test_update_user_profile(self):
#         """TEST UPDATING THE USER PROFILE FOR AUTHENTICATED USER"""
#         payload = {'name': 'new name', 'password': 'newpassword'}
#
#         res = self.client.patch(ME_URL, payload)
#
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.name, payload['name'])
#         self.assertEqual(self.user.check_password(payload['password']))
#         self.assertEqual(res.status_code, status.HTTP_200_OK)

