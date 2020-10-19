from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Feedback


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        exclude = ['created_date']

    def clean_email(self):
        data = self.cleaned_data['email']
        if "@softcatalyst.com" not in data:
            raise ValidationError("Only softcatalyst.com emails are allowed")
        return data
