import unittest
from unittest import mock

from django.core.validators import MinLengthValidator, MaxLengthValidator

from apps.core.serializers import PersianErrorMessages


class PersianErrorMessagesTestCase(unittest.TestCase):

    @mock.patch('apps.core.serializers.PersianErrorMessages.required_message')
    def test_get_messages_with_required_message(self, mock_required_message):
        field_model_detail = {'validators': [MinLengthValidator(limit_value=10), MaxLengthValidator(limit_value=20)]}
        persian_error_messages = PersianErrorMessages(field_model_detail)

        mock_required_message.return_value = {'required': 'این فیلد اجباری است.'}

        messages = persian_error_messages.get_messages()

        self.assertIsNotNone(messages)
        self.assertIsNot(messages, {})

    @mock.patch('apps.core.serializers.PersianErrorMessages.min_length_message')
    def test_get_messages_with_min_length_message(self, mock_min_length_message):
        field_model_detail = {'validators': [MinLengthValidator(limit_value=10), MaxLengthValidator(limit_value=20)]}
        persian_error_messages = PersianErrorMessages(field_model_detail)

        mock_min_length_message.return_value = {'min_length': 'حداقل مجاز کارکتر 10 است.'}

        messages = persian_error_messages.get_messages()

        self.assertIsNotNone(messages)
        self.assertIsNot(messages, {})

    @mock.patch('apps.core.serializers.PersianErrorMessages.max_length_message')
    def test_get_messages_with_max_length_message(self, mock_max_length_message):
        field_model_detail = {'validators': [MinLengthValidator(limit_value=10), MaxLengthValidator(limit_value=30)]}
        persian_error_messages = PersianErrorMessages(field_model_detail)

        mock_max_length_message.return_value = {'max_length': 'حداکثر مجاز کارکتر 30 است.'}

        messages = persian_error_messages.get_messages()

        self.assertIsNotNone(messages)
        self.assertIsNot(messages, {})

    def test_required_message(self):
        messages = PersianErrorMessages.required_message()

        self.assertEqual(messages, {'required': 'این فیلد اجباری است.'})

    def test_min_length_message(self):
        field_model_detail = {'validators': [MinLengthValidator(limit_value=10), MaxLengthValidator(limit_value=20)]}
        persian_error_messages = PersianErrorMessages(field_model_detail)

        message = persian_error_messages.min_length_message()

        self.assertEqual(message, {'min_length': 'حداقل مجاز کارکتر 10 است.'})

    def test_max_length_message(self):
        field_model_detail = {'validators': [MinLengthValidator(limit_value=10), MaxLengthValidator(limit_value=20)]}
        persian_error_messages = PersianErrorMessages(field_model_detail)

        message = persian_error_messages.max_length_message()

        self.assertEqual(message, {'max_length': 'حداکثر مجاز کارکتر 20 است.'})
