from django.urls import path
from . import views


urlpatterns = [
    path('', views.academics, name='academics'),
    path('submit-information-request/', views.submit_information, name='submit_information'),
    path('program/', views.program, name='program'),
]