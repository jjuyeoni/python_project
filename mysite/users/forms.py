import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=11, min_length=9)
    username = forms.CharField(max_length=50) 

    def clean_email(self):
        email = self.cleaned_data['email']
        if not re.match(r'^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}+$', email):
            raise forms.ValidationError("이메일은 영어(대문자, 소문자), 언더바(_), 숫자만 가능합니다.")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("이미 사용 중인 이메일입니다.")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) > 50:
            raise forms.ValidationError("사용자 이름은 50자 이하여야 합니다.")
        return username
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.isdigit():
            raise forms.ValidationError("전화번호는 숫자만 입력 가능합니다.")
        if len(phone_number) < 9 or len(phone_number) > 11:
            raise forms.ValidationError("전화번호는 9자에서 11자 사이로 입력해야 합니다.")
        return phone_number

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')

class LoginForm(forms.Form):
    email = forms.CharField(
        max_length=100, required=True, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "이메일"}))
    password = forms.CharField(
        max_length=30, required=True, widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "패스워드"})
    )
    


