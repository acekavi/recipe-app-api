from django import urls
from django.http import response
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@a.com",
            password="admin123",
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email="user@a.com",
            password="user123456",
            name='Full Name',
        )

    def test_users_listed(self):
        # Test if users are listed
        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_change_page(self):
        # Checking if the user edit page works
        url = reverse('admin:core_user_change', args=[self.user.id])
        # /admin/core/user/1
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_create_user_page(self):
        url = reverse('admin:core_user_add')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
