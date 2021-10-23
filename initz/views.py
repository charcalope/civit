from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.urls import path, reverse_lazy
from .forms import InitiativeForm, DonateForm, CreateExpenseForm, StatusUpdateForm, \
    CreateDocumentForm, CreateAnnotationForm
from django.contrib.auth.decorators import login_required
from accounts.models import User
from django.views.generic.edit import CreateView, DeleteView, UpdateView
import qrcode
from io import BytesIO
import base64

from .models import Initiative, Donation, Expense, StatusUpdate, LegislatorGroup, \
    MeetingRequest, Legislator, Document, Annotation

def generateQRCode(url):
    pil_img = qrcode.make(url).resize((150,150))
    img_io = BytesIO()
    pil_img.save(img_io, 'PNG')
    img_base64 = base64.b64encode(img_io.getvalue()).decode("utf-8")
    return img_base64

# Create your views here.
@login_required
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
        initiative.qrcode = generateQRCode("https://www.youtube.com/")
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

# CONTROL PANEL FUNCTIONALITY

@login_required
def homepanel(request, pk):
    initiative = Initiative.objects.get(pk=pk)
    return render(request, 'controlpanel/panelhome.html', {'initiative': initiative})

@login_required
def create_expense(request, pk):
    initiative = Initiative.objects.get(pk=pk)
    if request.method == 'GET':
        return render(request, 'controlpanel/create_expense.html', {'initiative': initiative, 'form': CreateExpenseForm})
    else:
        form = CreateExpenseForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            form_title = data['expense_title']
            form_desc = data['description']
            form_amount = data['amount']

            new_expense = Expense(initiative=initiative,
                                  reporter=request.user,
                                  title=form_title,
                                  description=form_desc,
                                  amount=form_amount)

            new_expense.save()

            return redirect('homepanel', pk=initiative.pk)

@login_required
def status_panel(request, pk):
    initiative = Initiative.objects.get(pk=pk)
    if request.method == 'GET':
        return render(request, 'controlpanel/viewstatus.html', {'initiative': initiative, 'form': StatusUpdateForm})
    else:
        form = StatusUpdateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            status = data['status']

            new_status_update = StatusUpdate(initiative=initiative,
                                            poster=request.user,
                                            text_content=status)

            new_status_update.save()

            return redirect('statuspanel', pk=initiative.pk)

@login_required
def delete_status(request, init_pk, status_pk):
    statusUpdate = StatusUpdate.objects.get(pk=status_pk).delete()
    return redirect('statuspanel', pk=init_pk)

@login_required
def expenses_panel(request, pk):
    initiative = Initiative.objects.get(pk=pk)
    return render(request, 'controlpanel/viewexpenses.html', {'initiative': initiative})

@login_required
def docs_panel(request, pk):
    initiative = Initiative.objects.get(pk=pk)
    documents = Document.objects.filter(initiative=initiative)
    return render(request, 'controlpanel/viewdocs.html', {'initiative': initiative,
                                                          'documents': documents})

@login_required
def people_panel(request, pk):
    initiative = Initiative.objects.get(pk=pk)
    return render(request, 'controlpanel/viewpeople.html', {'initiative': initiative})

@login_required
def meeting_requests_panel(request, pk):
    initiative = Initiative.objects.get(pk=pk)
    groups = LegislatorGroup.objects.all()

    if request.method == 'POST':
        query = request.POST.get('group_id')
        group = LegislatorGroup.objects.get(pk=query)

        legislators = group.legislators.all()

        packets = []

        for legislator in legislators:
            new_packet = dict()

            meeting_request_results = MeetingRequest.objects.filter(initiative=initiative, legislator=legislator)
            if len(meeting_request_results) > 0:
                existing_request = True
                meeting_request = meeting_request_results[0]
                if meeting_request.accepted:
                    status = 'Approved'
                elif meeting_request.denied:
                    status = 'Denied'
                else:
                    status = 'No Response'
            else:
                existing_request = False
                status = 'No Request Yet'

            new_packet['legislator'] = legislator
            new_packet['status'] = status
            new_packet['existing_request'] = existing_request

            packets.append(new_packet)

        return render(request, 'controlpanel/viewmeeting_requests.html', {'initiative': initiative,
                                                                          'groups': groups,
                                                                          'packets': packets})


    return render(request, 'controlpanel/viewmeeting_requests.html', {'initiative': initiative,
                                                                      'groups': groups})
@login_required()
def new_meeting_request_individual(request, init_pk, leg_pk):
    initiative = Initiative.objects.get(pk=init_pk)
    legislator = Legislator.objects.get(pk=leg_pk)

    new_meeting_request_object = MeetingRequest(initiative=initiative,
                                                requesting_organizer=request.user,
                                                legislator=legislator)
    new_meeting_request_object.save()

    # TODO: email functionality
    print("Email sent.")

    return redirect('meetingreqspanel', init_pk)

@login_required
def manageorganizers(request, pk):
    initiative = Initiative.objects.get(pk=pk)
    if request.method == 'GET':
        users = list(User.objects.all())
        print(users)
        organizers = []
        organizers.extend(initiative.organizers.all())
        organizers.append(initiative.primary_organizer)
        print(organizers)
        for user in users:
            if user in organizers:
                users.remove(user)
        return render(request, 'controlpanel/manageorganizers.html', {'initiative': initiative,
                                                                      'users': users})
    else:
        user_pk = request.POST.get('user_select')
        user = User.objects.get(pk=user_pk)
        initiative.organizers.add(user)
        return redirect(request.META.get('HTTP_REFERER'))

def create_document(request, pk):
    initiative = Initiative.objects.get(pk=pk)
    if request.method == 'GET':
        return render(request, 'controlpanel/create_document.html', {'initiative': initiative,
                                                                     'form':CreateDocumentForm})
    else:
        form = CreateDocumentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            new_document = Document(initiative=initiative,
                                    posting_organizer=request.user,
                                    doc_url=data['doc_url'],
                                    title=data['doc_title'],
                                    description=data['description'])
            new_document.save()

            return redirect('homepanel', initiative.pk)

@login_required
def create_annotation(request, init_pk, doc_pk):
    initiative = Initiative.objects.get(pk=init_pk)
    document = Document.objects.get(pk=doc_pk)
    if request.method == 'GET':
        return render(request, 'controlpanel/create_annotation.html', {'initiative': initiative,
                                                                       'form': CreateAnnotationForm})
    else:
        form = CreateAnnotationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            new_annotation = Annotation(initiative=initiative,
                                        document=document,
                                        annotating_organizer=request.user,
                                        excerpt=data['excerpt'],
                                        comment=data['comment'])
            new_annotation.save()

            return redirect('homepanel', initiative.pk)
