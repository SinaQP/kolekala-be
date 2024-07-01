from rest_framework import serializers

from apps.core.models import Setting
from apps.core.utility import PersianErrorMessages


class ModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, )

    class Meta:
        extra_kwargs = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_fields_list()
        self._append_messages()

    def _set_fields_list(self):
        try:
            self.fields_list = [*self.Meta.fields]
        except AttributeError:
            self.fields_list = []
            self.Meta.fields = ['id']

    def _append_messages(self):
        self._validate_extra_kwargs()
        setting = Setting.get_by_primary_key(1)
        if setting and setting.language == "fa":
            self._add_persian_error_messages_to_model_fields()

    def _add_persian_error_messages_to_model_fields(self):
        for model_field in self.fields_list:
            field_model_detail = self._get_field_model_detail(model_field)
            if not field_model_detail:
                return None

            persian_error_messages = PersianErrorMessages(field_model_detail)
            messages = persian_error_messages.get_messages()
            self.Meta.extra_kwargs.update({model_field: {'error_messages': messages}})

    def _get_field_model_detail(self, model_field):
        try:
            field_model_detail = self.Meta.model.__dict__[model_field].field.__dict__
        except AttributeError:
            return None
        return field_model_detail

    def _validate_extra_kwargs(self):
        try:
            self.Meta.extra_kwargs = {**self.Meta.extra_kwargs}
        except AttributeError:
            self.Meta.extra_kwargs = {}


class Serializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._append_message()

    def _append_message(self):
        for field_name,field in self.fields.items():
            self._set_error_messages(field)


    def _set_error_messages(self, field):
        persian_error_message_class = PersianErrorMessages(field)
        field.error_messages = persian_error_message_class.get_messages()

