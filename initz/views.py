from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.urls import path
from .forms import InitiativeForm

from .models import Initiative

# Create your views here.
def create(request):
    if request.method == 'GET':
        return render(request, 'initiative/create.html', {'form': InitiativeForm})
    else:
        form = InitiativeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_initiative = Initiative(primary_organizer=request.user,
                                        title=data['title'],
                                        problem_statement=data['problem_statement'],
                                        people_impact=data['people_impact'],
                                        legislative_scope=data['legislative_scope'],
                                        type=data['type'])
            new_initiative.save()

            tag_list = data['tags']
            tag_string = ', '.join(tag_list)
            new_initiative.tags = tag_string

            return redirect('landing')
