from django.contrib.auth import forms as auth_forms
from django.utils.translation import gettext_lazy as _
from django import forms
from accounts.models import Profile

class AdminSecurityEditForm(auth_forms.PasswordChangeForm):
    error_messages ={
        "password_incorrect":_("رمز قبلی شما اشتباه وارد شده لطفا تصحیح نمایید"),
        "password_mismatch":_("دو رمز ورودی با هم تطابق ندارند لطفا تصحیح نمایید")
    }

    def __init__(self, *args, **kwargs):
     super().__init__(*args, **kwargs)     
     self.fields["old_password"].widget.attrs['class'] = 'form-control text-center'
     self.fields["old_password"].widget.attrs['placeholder'] = 'رمز قبلی خود را وارد کنید' 
     self.fields["new_password1"].widget.attrs['class'] = 'form-control text-center'
     self.fields["new_password1"].widget.attrs['placeholder'] = 'رمز جدید خود را وارد کنید'
     self.fields["new_password2"].widget.attrs['class'] = 'form-control text-center'
     self.fields["new_password2"].widget.attrs['placeholder'] = 'رمز جدید خود را تایید کنید'


class AdminProfileEditForm(forms.ModelForm):
   class Meta:
        model=Profile
        fields =[
            "first_name",
            "last_name",
            "phone_number"
        ]
   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'نام خود را وارد نمایید'
        self.fields['last_name'].widget.attrs['class'] = 'form-control '
        self.fields['last_name'].widget.attrs['placeholder'] = 'نام خانوادگی را وارد نمایید'
        self.fields['phone_number'].widget.attrs['class'] = 'form-control text-center'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'شماره همراه را وارد نمایید'