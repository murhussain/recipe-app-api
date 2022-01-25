from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')

class PublicTagApiTests(TestCase):
    """TEST THAT PUBLICITY AVAILABLE TAGS API"""

    def setup(self):
        self.client = APIClient()

    def test_login_requirement(self):
        """TEST THAT LOGIN IS REQUIRED FOR RETRIEVING THE TAGS"""

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# class PrivateTagsApiTests(TestCase):
#     """TEST THE AUTHORIZED USER TAGS API"""
#
#     def setup(self):
#         self.user = get_user_model().objects.create_user(
#             'mur@test.com',
#             'pass123'
#         )
#         self.client = APIClient()
#         self.client.force_authenticate(self.user)
#
#     def test_retrieve_tags(self):
#         """TEST RETRIEVE TAGS"""
#         tag.object.create(user=self.user, name='vegan')
#         tag.object.create(user=self.user, name='salt')
#
#         res = self.client.get(TAGS_URL)
#
#         tags = Tag.objects.all().order_by('-name')
#         serializer = TagSerializer(tags, many=True)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, serializer.data)
#
#     def test_tags_limited_to_user(self):
#         """TEST THAT RETURNED ARE FOR AUTHENTICATED USER"""
#         user2 = get_user_model().objects.create_user(
#             'mur@test.com',
#             'test123'
#         )
#         Tag.objects.create(user=user2, name='fruity')
#         tag = Tag.objects.create(name='Comfort Food', user=self.user)
#
#         res = self.client.get(TAGS_URL)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(res.data), 1)
#         self.assertEqual(res.data[0]['name'], tag.name)
#
#     def test_create_tag_successful(self):
#         """TEST CREATING A NEW TAG"""
#         payload = {'name': 'test tag'}
#         self.client.post(TAGS_URL, payload)
#
#         exists = Tag.objects.filter(
#             user=self.user,
#             name=payload('name')
#         ).exists()
#         self.assertTrue(exists)
#
#     def test_create_tag_invalid(self):
#         """TEST CREATING NEW TAGS WITH INVALID PAYLOAD"""
#         payload = {'name': ''}
#         res = self.client.post(TAGS_URL, payload)
#
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)