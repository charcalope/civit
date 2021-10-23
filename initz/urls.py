from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.create, name='create'),
    path('<pk>/viewinit', views.view_public_init, name='viewinit'),
    path('<pk>/sign', views.sign, name='sign'),
    path('<pk>/feed', views.view_status_feed, name='viewfeed'),
    path('<pk>/viewexpenses', views.view_expenses, name='viewexpenses'),
    path('<pk>/viewdocs', views.view_documents, name='viewdocs'),
    path('<pk>/viewpeople', views.view_people, name='viewpeople'),
    path('<pk>/viewmeetingreqs', views.view_meeting_requests, name='viewmeetingreqs'),
    # control panel
    path('<pk>/homepanel', views.homepanel, name='homepanel'),
    path('<pk>/expensepanel', views.expenses_panel, name='expensepanel'),
    path('<pk>/peoplepanel', views.people_panel, name='peoplepanel'),
    path('<pk>/docspanel', views.docs_panel, name='docspanel'),
    path('<pk>/statuspanel', views.status_panel, name='statuspanel'),
    path('<pk>/create_expense', views.create_expense, name='create_expense'),
    path('<pk>/meetingrequests_panel', views.meeting_requests_panel, name='meetingreqspanel'),
    path('<pk>/manageorganizers', views.manageorganizers, name='manageorganizers'),
    path('<init_pk>/<status_pk>/delete_status', views.delete_status, name='delete_status'),
    path('<init_pk>/<leg_pk>/create_req', views.new_meeting_request_individual, name='createreqind'),
    path('<pk>/create_doc', views.create_document, name='createdoc'),
    path('<init_pk>/<doc_pk>/create_annotation', views.create_annotation, name='createannotation'),

]
