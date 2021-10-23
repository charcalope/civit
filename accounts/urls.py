from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('<pk>/editprofile', views.UpdateProfileView.as_view(), name='editprofile'),
    path('<pk>/view_profile', views.public_profile_page, name='viewprofile'),
]