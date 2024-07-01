import unittest
from unittest import mock
from rest_framework import serializers

from apps.core.models import Setting
from apps.core.serializers import ModelSerializer, Serializer
from apps.core.utility import PersianErrorMessages


class ModelSerializerTestCase(unittest.TestCase):
    def test_init(self):
        serializer = ModelSerializer()

        self.assertEqual(serializer.fields_list, ['id'])

    @staticmethod
    def test_append_messages():
        serializer = ModelSerializer()
        serializer.Meta.model = Setting

        Setting.objects.create(language='fa')
        with mock.patch('apps.core.serializers.ModelSerializer._validate_extra_kwargs') as mock_validate_extra_kwargs:

            serializer._append_messages()

            mock_validate_extra_kwargs.assert_called()

        with mock.patch('apps.core.serializers.ModelSerializer._add_persian_error_messages_to_model_fields') \
                as mock_add_persian_error_messages_to_model_fields:

            serializer._append_messages()

            mock_add_persian_error_messages_to_model_fields.assert_called_once()

    def test_add_persian_error_messages_to_model_fields(self):
        with mock.patch('apps.core.serializers.ModelSerializer._validate_extra_kwargs') as mock_validate_extra_kwargs:
            serializer = ModelSerializer()
            serializer.Meta.model = Setting

            serializer._add_persian_error_messages_to_model_fields()

            mock_validate_extra_kwargs.assert_called_once()

            for model_field in serializer.fields_list:
                self.assertEqual(serializer.extra_kwargs[model_field], {'error_messages': PersianErrorMessages()
                                 .get_messages()})

    def test_validate_extra_kwargs(self):
        serializer = ModelSerializer()
        serializer._validate_extra_kwargs()

        self.assertIsNotNone(serializer.Meta.extra_kwargs)
        self.assertIsNot(serializer.Meta.extra_kwargs, {})


class SerializerTests(unittest.TestCase):
    def test_custom_error_messages(self):
        class TestSerializer(Serializer):
            name = serializers.CharField(required=True)

        serializer = TestSerializer(data={})
        self.assertFalse(serializer.is_valid())

        self.assertIsNotNone(serializer.errors)

    def test_custom_error_messages_multiple_fields(self):
        class TestSerializer(Serializer):
            name = serializers.CharField(required=True)
            email = serializers.EmailField(required=True)

        serializer = TestSerializer(data={})
        self.assertFalse(serializer.is_valid())

        self.assertIsNotNone(serializer.errors)
