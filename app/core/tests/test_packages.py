"""
Test core package API
"""
from django.test import TestCase
from core.models import Package


class PackageTests(TestCase):
    def test_create_new_package(self):
        title = "test package"
        data = 12345

        package = Package.objects.create(
            title=title,
            data=data
        )

        self.assertEqual(package.title, title)
        self.assertEqual(package.data, data)
