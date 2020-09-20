from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'نام و نام خانوادگی'})
        self.fields['email'].widget.attrs.update({'placeholder': 'آدرس ایمیل'})
        self.fields['body'].widget.attrs.update({'placeholder': 'متن نظر'})
