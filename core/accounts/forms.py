from django.contrib.auth import forms as auth_form
from django.forms import ValidationError

class AuthenticationForm(auth_form.AuthenticationForm):
    def confirm_login_allowed(self, user):
        super(AuthenticationForm,self).confirm_login_allowed(user)
        # if not user.is_verified:
        #     raise ValidationError(
        #         self.error_messages["user is not verified"],
        #     )
       