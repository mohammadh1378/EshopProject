from django import forms
from django.contrib.auth.models import User
from django.core import validators

from eshop_account.models import Profile


class LoginForm(forms.Form):
    user_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا نام کاربری خود را وارد نمایید'}),
        label='نام کاربری'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'لطفا کلمه عبور خود را وارد نمایید'}),
        label='کلمه ی عبور'
    )

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        is_exists_user = User.objects.filter(username=user_name).exists()
        if not is_exists_user:
            raise forms.ValidationError('کاربری با مشخصات وارد شده ثبت نام نکرده است')

        return user_name


class RegisterForm(forms.Form):
    user_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا نام کاربری خود را وارد نمایید'}),
        label='نام کاربری',
        validators=[
            validators.MaxLengthValidator(limit_value=20,
                                          message='تعداد کاراکترهای وارد شده نمیتواند بیشتر از 20 باشد'),
            validators.MinLengthValidator(8, 'تعداد کاراکترهای وارد شده نمیتواند کمتر از 8 باشد')
        ]
    )

    email = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا ایمیل خود را وارد نمایید'}),
        label='ایمیل',
        validators=[
            validators.EmailValidator('ایمیل وارد شده معتبر نمیباشد')
        ]
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'لطفا کلمه عبور خود را وارد نمایید'}),
        label='کلمه ی عبور'
    )

    re_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'لطفا تکرار کلمه عبور خود را وارد نمایید'}),
        label='تکرار کلمه ی عبور'
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        is_exists_user_by_email = User.objects.filter(email=email).exists()
        if is_exists_user_by_email:
            raise forms.ValidationError('ایمیل وارد شده تکراری میباشد')

        if len(email) > 50:
            raise forms.ValidationError('تعداد کاراکترهای ایمیل باید کمتر از 50 باشد')

        return email

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        is_exists_user_by_username = User.objects.filter(username=user_name).exists()

        if is_exists_user_by_username:
            raise forms.ValidationError('این کاربر قبلا ثبت نام کرده است')

        return user_name

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        print(password)
        print(re_password)

        if password != re_password:
            raise forms.ValidationError('کلمه های عبور مغایرت دارند')

        return password


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': 'ایمیل', 'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'placeholder': 'نام کاربری', 'class': 'form-control'})


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'phone_number', 'address', 'postal_code', 'city')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'نام', 'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'نام خانوادگی', 'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'placeholder': 'تلفن', 'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'placeholder': 'آدرس', 'class': 'form-control'})
        self.fields['city'].widget.attrs.update({'placeholder': 'شهر', 'class': 'form-control'})
        self.fields['postal_code'].widget.attrs.update({'placeholder': 'کد پستی', 'class': 'form-control'})

# class ProfileForm(forms.Form):
#     # user_name = forms.CharField(
#     #     widget=forms.TextInput(attrs={'placeholder': 'لطفا نام کاربری خود را وارد نمایید', 'class': 'form-control'}),
#     #     label='نام کاربری',
#     #     # value=Profile.user.username,
#     #     validators=[
#     #         validators.MaxLengthValidator(limit_value=20,
#     #                                       message='تعداد کاراکترهای وارد شده نمیتواند بیشتر از 20 باشد'),
#     #         validators.MinLengthValidator(8, 'تعداد کاراکترهای وارد شده نمیتواند کمتر از 8 باشد')
#     #     ]
#     # )
#
#     email = forms.CharField(
#         widget=forms.TextInput(attrs={'placeholder': 'لطفا ایمیل خود را وارد نمایید', 'class': 'form-control'}),
#         label='ایمیل',
#         validators=[
#             validators.EmailValidator('ایمیل وارد شده معتبر نمیباشد')
#         ]
#     )
#
#     first_name = forms.CharField(
#         widget=forms.TextInput(attrs={'placeholder': 'لطفا نام خود را وارد نمایید', 'class': 'form-control'}),
#         label='نام',
#     )
#     last_name = forms.CharField(
#         widget=forms.TextInput(attrs={'placeholder': 'لطفا نام خانوادگی خود را وارد نمایید', 'class': 'form-control'}),
#         label='نام خانوادگی',
#     )
#     phone_number = forms.CharField(
#         widget=forms.TextInput(attrs={'placeholder': 'لطفا شماره تلفن خود را وارد نمایید', 'class': 'form-control'}),
#         label='شماره تلفن',
#     )
#     address = forms.CharField(
#         widget=forms.TextInput(attrs={'placeholder': 'لطفا آدرس خود را وارد نمایید', 'class': 'form-control'}),
#         label='آدرس',
#     )
#     postal_code = forms.CharField(
#         widget=forms.TextInput(attrs={'placeholder': 'لطفا کد پستی خود را وارد نمایید', 'class': 'form-control'}),
#         label='کد پستی',
#     )
#     city = forms.CharField(
#         widget=forms.TextInput(attrs={'placeholder': 'لطفا شهر خود را وارد نمایید', 'class': 'form-control'}),
#         label='شهر',
#     )
#
#     # def clean_email(self):
#     #     email = self.cleaned_data.get('email')
#     #     is_exists_user_by_email = Profile.objects.filter(email=email).exists()
#     #     same_user = User.objects.filter(email=email)
#     #     if is_exists_user_by_email and email is not :
#     #         raise forms.ValidationError('ایمیل وارد شده تکراری میباشد')
#     #
#     #     if len(email) > 50:
#     #         raise forms.ValidationError('تعداد کاراکترهای ایمیل باید کمتر از 50 باشد')
#     #
#     #     return email
#
#
#     def clean_email(self, user):
#         email = self.cleaned_data.get('email')
#         is_exists_user_by_email = User.objects.filter(email=email).exists()
#
#         if is_exists_user_by_email and :
#             raise forms.ValidationError('ایمیل وارد شده تکراری میباشد')
#
#         if len(email) > 50:
#             raise forms.ValidationError('تعداد کاراکترهای ایمیل باید کمتر از 50 باشد')
#
#         return email
