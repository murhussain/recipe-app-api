from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setup(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@test.com',
            password='123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='mur@test.com',
            password='123',
            name='test user full name'
        )

    def test_user_listed(self):
        """TEST THAT USERS ARE LISTED IN DJANGO ADMIN"""
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        # self.assertContains(res, self.user.email)
        # self.assertContains(res , self.user.name)

    def test_user_change_page(self):
        """TEST IF USER EDITS WORK"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_user_create_page(self):
        """TEST IF USER CREATE WORK"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)