from django import forms
from crispy_forms.helper import FormHelper
from django.core.exceptions import ValidationError

from .models import Post, Feedback


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class FeedbackForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_show_labels = True
    helper.html5_required = True
    helper.form_method = 'post'
    helper.form_class = 'blueForms'

    class Meta:
        model = Feedback
        exclude = ['created_date']

    def clean_email(self):
        data = self.cleaned_data['email']
        if "@softcatalyst.com" not in data:
            raise ValidationError("Only softcatalyst.com emails are allowed")
        return data
