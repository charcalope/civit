from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.create, name='create'),
    path('<pk>/viewinit', views.view_public_init, name='viewinit')
]
