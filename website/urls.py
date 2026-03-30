from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Index, name='index'),
    path('about/', views.about, name="about"),
    path('students-life/', views.students_life, name="students_life"),
    path('contact/', views.contect, name="contact"),
    path('submit-visit-request/', views.submit_campus_visit_request, name="submit_campus_visit"),
    path('alumni/', views.alumni, name='alumni'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms-of-service/', views.term_services, name='term_services')
]
