from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Contact, Comment


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ('name', 'phone', 'email', 'subject', 'message',)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-Crispy_ContactForm'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('send', 'Send Email'))





class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'comment',)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-Crispy_ContactForm'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('send', 'Submit'))
