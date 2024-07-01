from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db.utils import OperationalError
from apps.core.models import Setting


class PersianErrorMessages:
    def __init__(self, field_model_detail: dict):
        self.field_model_detail = field_model_detail
        self._set_field_validators()
        self.merged_message = {}

    def get_messages(self):
        self.merged_message.update(self.max_length_message())
        self.merged_message.update(self.blank_message())
        self.merged_message.update(self.required_message())
        self.merged_message.update(self.min_length_message())
        return self.merged_message

    def _set_field_validators(self):
        try:
            self.field_validators = self.field_model_detail['validators']
        except TypeError:
            self.field_validators = []

    @staticmethod
    def required_message():
        return {'required': 'این فیلد اجباری است.'}

    @staticmethod
    def blank_message():
        return {'blank': f'این فیلد اجباری است.'}

    def min_length_message(self):
        if self.min_length_from_validator():
            return self.min_length_from_validator()
        return self.min_length_from_model()

    def min_length_from_validator(self):
        min_length_validator_index = self.find_validator_index(validator=MinLengthValidator)
        if min_length_validator_index is not None:
            limited_value = self.field_validators[min_length_validator_index].limit_value
            return self.create_min_length_message(limited_value)

    def min_length_from_model(self):
        try:
            if self.field_model_detail.min_length is not None:
                limited_value = self.field_model_detail.min_length
                return self.create_min_length_message(limited_value)
            return {}
        except AttributeError:
            return {}
    def max_length_message(self):
        if self.max_length_from_validator():
            return self.max_length_from_validator()
        return self.max_length_from_model()

    def max_length_from_validator(self):
        max_length_validator_index = self.find_validator_index(validator=MaxLengthValidator)
        if max_length_validator_index is not None:
            limited_value = self.field_validators[max_length_validator_index].limit_value
            return self.create_max_length_message(limited_value)
        return {}

    def max_length_from_model(self):
        try:
            if self.field_model_detail.max_length is not None:
                limited_value = self.field_model_detail.max_length
                return self.create_max_length_message(limited_value)
            return {}
        except AttributeError:
            return {}
    def find_validator_index(self, validator):
        index = 0
        for field_validator in self.field_validators:
            if isinstance(field_validator, validator):
                return index
            index += 1
        return None

    @staticmethod
    def create_max_length_message(limited_value):
        return {'max_length': f'حداکثر مجاز کارکتر {limited_value} است.'}

    @staticmethod
    def create_min_length_message(limited_value):
        return {'min_length': f'حداقل مجاز کارکتر {limited_value} است.'}

def validation_message(en_message="", fa_message=""):
    try:
        setting = Setting.get_by_primary_key(1)
        if setting and setting.language == "fa":
            return fa_message
        return en_message
    except OperationalError:
        return en_message
