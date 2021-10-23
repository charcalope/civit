from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.urls import path
from .forms import InitiativeForm

from .models import Initiative, Tag

# Create your views here.
def create(request):
    if request.method == 'GET':
        return render(request, 'initiative/create.html', {'form': InitiativeForm})
    else:
        form = InitiativeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            tag_list = []
            selected_tags = data['tags']
            for tag in selected_tags:
                tag_object = Tag.objects.filter(tag_description=tag)
                tag_list.append(tag_object[0])
            new_initiative = Initiative(primary_organizer=request.user,
                                        title=data['title'],
                                        problem_statement=data['problem_statement'],
                                        people_impact=data['people_impact'],
                                        legislative_scope=data['legislative_scope'],
                                        type=data['type'])
            new_initiative.save()
            for tag in tag_list:
                new_initiative.tags.add(tag)
            new_initiative.save()
            return redirect('landing')
