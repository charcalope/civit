from django.urls import path

from . import views

urlpatterns = [
    path('expenseguide/', views.expense_guide, name='expenseguide'),
    path('legislativeguide/', views.legislative_guide, name='legislativeguide'),
]