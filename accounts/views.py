from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, UserUpdateForm
from .models import User
from initz.models import Initiative
from django.views.generic.edit import UpdateView, CreateView
from django.forms.models import modelform_factory

from initz.models import Initiative

# Create your views here.

def home(request):
    initiatives = Initiative.objects.all()
    return render(request, 'home_a.html', {'initiatives':initiatives})

@login_required
def dashboard(request):
    my_organizer_inits = set()
    my_supporting_inits = set()

    initiatives = Initiative.objects.all()

    for init in initiatives:
        if (init.primary_organizer == request.user) or (request.user in init.organizers.all()):
            my_organizer_inits.add(init)
        elif (request.user in init.supporters.all()):
            my_supporting_inits.add(init)

    my_organizer_inits = list(my_organizer_inits)
    my_supporting_inits = list(my_supporting_inits)

    return render(request, 'dash/dashboard.html', {'support_inits': my_supporting_inits,
                                                   'organizer_inits': my_organizer_inits})

def register(request):
    if request.method == 'GET':
        return render(request, 'registration/register.html', {'form': SignUpForm})
    else:
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('landing')

class UpdateProfileView(UpdateView):
    model = User
    form_class = modelform_factory(User, fields=['first_name',
                                                 'last_name',
                                                 'bio',
                                                 'profile_picture'])
    success_url = reverse_lazy('dashboard')
    template_name = 'registration/edit_profile.html'


def public_profile_page(request, pk):
    other_user = User.objects.get(id=pk)
    return render(request, 'registration/public_profile.html', {'other_user': other_user})
