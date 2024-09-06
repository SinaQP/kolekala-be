from django.contrib.auth.password_validation import UserAttributeSimilarityValidator, MinimumLengthValidator, \
    CommonPasswordValidator, NumericPasswordValidator
from django.utils.translation import gettext_lazy as _


class CustomUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    def get_help_text(self):
        return _('رمز عبور بسیار شبیه به اطلاعات کاربر است.')


class CustomMinimumLengthValidator(MinimumLengthValidator):
    def get_help_text(self):
        return _('رمز عبور باید حداقل ۸ کاراکتر باشد.')


class CustomCommonPasswordValidator(CommonPasswordValidator):
    def get_help_text(self):
        return _('رمز عبور بسیار رایج است.')


class CustomNumericPasswordValidator(NumericPasswordValidator):
    def get_help_text(self):
        return _('رمز عبور نمی‌تواند کاملاً عددی باشد.')
