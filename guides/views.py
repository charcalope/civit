from django.shortcuts import render

# Create your views here.

def expense_guide(request):
    return render(request, 'guides/expense_guide.html', {})

def legislative_guide(request):
    return render(request, 'guides/legislative_guide.html', {})
