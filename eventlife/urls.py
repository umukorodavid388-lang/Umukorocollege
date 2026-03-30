from django.urls import path
from . import views



urlpatterns = [
    path('<int:event_id>/like/', views.toggle_event_like, name='toggle_like'),
    path('api/calendar/', views.calendar_events, name='calendar_events'),
    path('', views.events, name='event'),
    path('events/category/<int:category_id>/', views.event_by_category, name='event_by_category'),
    path('events/details/<int:event_id>/', views.event_details, name='event_detail'),
]
