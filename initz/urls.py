from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.create, name='create'),
    path('<pk>/viewinit', views.view_public_init, name='viewinit'),
    path('<pk>/sign', views.sign, name='sign'),
    path('<pk>/homepanel', views.homepanel, name='homepanel'),
    path('<pk>/feed', views.view_status_feed, name='viewfeed'),
    path('<pk>/viewexpenses', views.view_expenses, name='viewexpenses'),
    path('<pk>/viewdocs', views.view_documents, name='viewdocs'),
    path('<pk>/viewpeople', views.view_people, name='viewpeople'),
    path('<pk>/viewmeetingreqs', views.view_meeting_requests, name='viewmeetingreqs'),

]
