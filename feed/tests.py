from django.test import TestCase

from .models import ShowType


class ShowTypeModelTests(TestCase):
    def setUp(self):
        self.test_show_type = ShowType()
        self.test_show_type.name = 'Test Show'
        self.test_show_type.save()

    def test_name_hex_color_get(self):
        self.assertEqual(self.test_show_type.name_hex_color, '#000000')

    def test_name_hex_color_set(self):
        self.test_show_type.name_hex_color = '#FFFFFF'
        self.test_show_type.save()
        self.assertEqual(self.test_show_type.name_color, self.test_show_type.maximum_name_color_value)

    def test_name_color_set_failure(self):
        self.test_show_type.name_color = self.test_show_type.maximum_name_color_value + 1000
        try:
            self.test_show_type.save()
            self.fail("Test should fail.")
        except AttributeError:
            pass

    def test_name_hex_color_get_failure(self):
        self.test_show_type.name_color = self.test_show_type.maximum_name_color_value + 1000
        try:
            test = self.test_show_type.name_hex_color
            self.fail("Test should fail.")
        except AttributeError:
            pass

    def test_name_hex_color_set_failure(self):
        try:
            self.test_show_type.name_hex_color = '#FFFFFFF'
            self.fail("Test should fail.")
        except AttributeError:
            pass