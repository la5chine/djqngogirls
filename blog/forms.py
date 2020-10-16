from django import forms
from crispy_forms.helper import FormHelper

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
        fields = "__all__"
