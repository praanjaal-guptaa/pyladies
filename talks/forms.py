from django import forms
from crispy_forms.helper  import FormHelper
from crispy_forms.layout  import Submit
from markitup.widgets  import MarkItUpWidget

from talks.models import Proposal, Suggestion


class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ('title', 'talk_type', 'abstract')
        widgets = {
            'abstract': MarkItUpWidget(),
          }

    def __init__(self, *args, **kwargs):
        super(ProposalForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.add_input(Submit('send', 'Submit'))
        self.helper.form_class = 'form-horizontal'


class SuggestForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ('title', 'talk_type', 'details')
        widgets = {
            'abstract': MarkItUpWidget(),
          }

    def __init__(self, *args, **kwargs):
        super(SuggestForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.add_input(Submit('send', 'Submit'))
        self.helper.form_class = 'form-horizontal'

