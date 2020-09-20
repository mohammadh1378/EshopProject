from django import forms
from .models import NewOrder


class UserNewOrderForm(forms.Form):
    product_id = forms.IntegerField(
        widget=forms.HiddenInput(),
    )

    count = forms.IntegerField(
        widget=forms.NumberInput(),
        initial=1
    )


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = NewOrder
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'city',
                  'postal_code', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'نام', 'class': 'important-field'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'نام خانوادگی', 'class': 'important-field'})
        self.fields['email'].widget.attrs.update({'placeholder': 'آدرس ایمیل', 'class': 'important-field'})
        self.fields['phone_number'].widget.attrs.update({'placeholder': 'شماره تلفن', 'class': 'important-field'})
        self.fields['city'].widget.attrs.update({'placeholder': 'شهر', 'class': 'important-field'})
        self.fields['postal_code'].widget.attrs.update({'placeholder': 'کد پستی', 'class': 'important-field'})
        self.fields['address'].widget.attrs.update({'placeholder': 'آدرس', 'class': 'important-field'})
