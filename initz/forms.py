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
    problem_statement = forms.CharField(label='What is the problem you see?', max_length=500)
    people_impact = forms.CharField(label='People impacted by this problem', max_length=500)
    legislative_scope = forms.CharField(label='What do you propose we could do?', max_length=500)
    tags = forms.CharField(label='Tags', widget=forms.SelectMultiple(choices=TAGS))
    type = forms.CharField(label='Type of legislation', widget=forms.Select(choices=TYPE))

class DonateForm(forms.Form):
    amount = forms.IntegerField(label="Donate Amount")

class CreateExpenseForm(forms.Form):
    expense_title = forms.CharField(max_length=200, label='Expense Title')
    description = forms.CharField(max_length=400, label='Description of Expense')
    amount = forms.IntegerField(label='Expense Amount')

class StatusUpdateForm(forms.Form):
    status = forms.CharField(max_length=1000, label='Status Description')

class CreateDocumentForm(forms.Form):
    doc_title = forms.CharField(max_length=200, label='Document Title')
    description = forms.CharField(max_length=400, label='Document Description')
    doc_url = forms.URLField(label='Google Drive Url')

class CreateAnnotationForm(forms.Form):
    excerpt = forms.CharField(widget=forms.Textarea, label='Quote a part of the Document')
    comment = forms.CharField(widget=forms.Textarea, label='Add an Annotation')
