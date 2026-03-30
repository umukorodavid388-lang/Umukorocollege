from django.urls import path
from . import views


urlpatterns = [
    path('', views.addmission, name='addmission'),
    path('submit-information-request/', views.submit_information_request, name='submit_information_request'),
    path('submit-campus-visit/', views.submit_campus_visit_request, name='submit_campus_visit_request'),
    path('campus-visits/', views.campus_visits, name='campus_visits'),
    path('information-requests/', views.information_requests, name='information_requests'),
]