from .models import Initiative
from django import forms

TAGS = [
    ('education', 'Education'),
    ('traffic', 'Traffic'),
    ('police', 'Law Enforcement'),
    ('parks', 'Public Parks'),
]

TYPE = [
    ('city', 'City'),
    ('state', 'State'),
]

class InitiativeForm(forms.Form):
    title = forms.CharField(label='Title of Legislation', max_length=200)
    problem_statement = forms.CharField(label='Bio', max_length=500)
    people_impact = forms.CharField(label='People impacted by this problem', max_length=500)
    legislative_scope = forms.CharField(label='What do you propose we could do?', max_length=500)
    tags = forms.CharField(label='Tags', widget=forms.SelectMultiple(choices=TAGS))
    type = forms.CharField(label='Type of legislation', widget=forms.Select(choices=TYPE))
