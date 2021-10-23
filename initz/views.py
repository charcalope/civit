from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.urls import path
from .forms import InitiativeForm, DonateForm
from django.contrib.auth.decorators import login_required

from .models import Initiative, Donation

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
            print(tag_list)
            new_initiative.tags = tag_list

            return redirect('viewinit', pk=new_initiative.pk)

@login_required
def view_public_init(request, pk):
    initiative = Initiative.objects.get(pk=pk)
    if request.method == "GET":
        return render(request, 'initiative/public_view_init.html', {'initiative': initiative, 'donate_form': DonateForm})
    else:
        form = DonateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_donation = Donation(donor=request.user,
                                        initiative=initiative,
                                        amount=data['amount'])
            new_donation.save()
            return redirect('viewinit', pk=initiative.pk)

@login_required
def sign(request, pk):
    initiative = Initiative.objects.get(pk=pk)
    initiative.supporters.add(request.user)
    initiative.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def homepanel(request, pk):
    initiative = Initiative.objects.get(pk=pk)
    return render(request, 'controlpanel/panelhome.html', {'initiative': initiative})

def view_status_feed(request, pk):
    initiative = Initiative.objects.get(pk=pk)
    return render(request, 'initiative/status_feed.html', {'initiative': initiative})

def view_expenses(request, pk):
    initiative = Initiative.objects.get(pk=pk)
    return render(request, 'initiative/expenses.html', {'initiative': initiative})

def view_documents(request, pk):
    initiative = Initiative.objects.get(pk=pk)
    return render(request, 'initiative/documents.html', {'initiative': initiative})

def view_people(request, pk):
    initiative = Initiative.objects.get(pk=pk)
    return render(request, 'initiative/people.html', {'initiative': initiative})

def view_meeting_requests(request, pk):
    initiative = Initiative.objects.get(pk=pk)
    return render(request, 'initiative/meeting_requests.html', {'initiative': initiative})