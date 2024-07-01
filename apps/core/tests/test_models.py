from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from ..models import Setting


class SettingTest(TestCase):
    setting = Setting()

    def test_get_by_primary_key(self):
        setting = Setting.objects.create(language='fa')

        created_setting = Setting.get_by_primary_key(setting.pk)
        self.assertEqual(created_setting, setting)

        non_exist_setting = Setting.get_by_primary_key(9999)
        self.assertIsNone(non_exist_setting)

    def test_language_required(self):
        with self.assertRaises(ValidationError):
            self.setting.language = None
            self.setting.full_clean()

    def test_language_valid_choice(self):
        with self.assertRaises(ValidationError):
            self.setting.language = 'invalid_choice'
            self.setting.full_clean()

    def test_duplicate_pk(self):
        setting = Setting.objects.create(language='fa')

        with self.assertRaises(IntegrityError):
            Setting.objects.create(pk=setting.pk)


