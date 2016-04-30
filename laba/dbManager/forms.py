from django import forms


class PartFrom(forms.Form):
    def __init__(self, context):
        self.choice_field = forms.ChoiceField(choices=context, required=True, label="Text")