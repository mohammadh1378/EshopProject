from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'min': '1',
            'max': '10'
        }),
        initial=1,

    )
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)
