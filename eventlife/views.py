from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import *
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models import Q
from django.contrib import messages
import datetime
import calendar
from django.utils import timezone as dj_timezone


@require_http_methods(["POST"])
def toggle_event_like(request, event_id):
    """Toggle like on an event"""
    try:
        event = get_object_or_404(Event, id=event_id)
        
        # Check if like already exists
        like = EventLike.objects.filter(event=event).first()
        
        if like:
            like.delete()
            liked = False
        else:
            EventLike.objects.create(event=event)
            liked = True
        
        return JsonResponse({
            'success': True,
            'liked': liked,
            'likes_count': event.get_likes_count()
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)



def events(request):
    event = Event.objects.all().order_by('-created_at')

    upcoming_featured_events = Event.objects.filter(
        featured=True,
        date__gte=timezone.now().date()  # only future events
    ).order_by('date')[:3]  # show top 3 featured events


    paginator = Paginator(event, 6)  # 6 events per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    query = request.GET.get('q')
    if query:
        event = event.filter(
            Q(title__icontains=query) |
            Q(date__icontains=query) |
            Q(location__icontains=query) |
            Q(eventcategories__text__icontains=query)
        )

    # Calendar initial data (server-side rendered)
    today = dj_timezone.localtime(dj_timezone.now())
    cal_year = int(request.GET.get('cal_year', today.year))
    cal_month = int(request.GET.get('cal_month', today.month))

    # events for calendar month
    cal_events_qs = Event.objects.filter(date__year=cal_year, date__month=cal_month).order_by('date')
    cal_days_events = {}
    for ev in cal_events_qs:
        day = ev.date.day
        cal_days_events.setdefault(day, []).append({
            'id': ev.id,
            'title': ev.title,
            'date': ev.date.isoformat(),
        })

    # weeks matrix for month (list of weeks, each week is list of ints, 0 means empty)
    cal_weeks = calendar.monthcalendar(cal_year, cal_month)


    context = {
        'event':event,
        'page_obj': page_obj,
        'upcoming_featured_events': upcoming_featured_events,   
        'cal_year': cal_year,
        'cal_month': cal_month,
        'cal_month_name': calendar.month_name[cal_month],
        'cal_weeks': cal_weeks,
        'cal_days_events': cal_days_events,
    }
    return render(request, 'event/events.html', context)


def event_by_category(request, category_id):
    category = get_object_or_404(EventCategory, id=category_id)


    context = {
        'events': events,
        'active_category': category
    }

    return render(request, 'event/events.html', context)


def event_details(request, event_id):
    event_details = get_object_or_404(Event, id=event_id)
    highlight = EventHighlight.objects.filter(event=event_details)
    shedule = EventSchedule.objects.filter(events=event_details)
    gallery = EventGallery.objects.filter(eventgallery=event_details).order_by('-created_date')
    organizer = EventOrganizer.objects.filter(event=event_details).first()
    
    # Get related events from same category (excluding current event)
    related_events = Event.objects.filter(
        eventcategories=event_details.eventcategories
    ).exclude(id=event_id).order_by('-date')[:5]

    if request.method == "POST":
        EventRegistration.objects.create(
        name=request.POST.get("name"),
        email=request.POST.get("email"),
        phone=request.POST.get("phone"),
        student_type=request.POST.get("student_type"),
        other_type=request.POST.get("other_type", "")
    )
        
        messages.success(request, 'Your event message was sent successfully')
        return redirect("event_detail", event_id=event_id)

    context = {
        "event_details": event_details,
        "highlight": highlight,
        "shedule": shedule,
        "gallery": gallery,
        "organizer": organizer,
        "related_events": related_events,
    }
    return render(request, 'event/event-details.html', context)


def calendar_events(request):
    """Return events for a given month as JSON.

    Query params:
      - year: 4-digit year (defaults to current year)
      - month: month number 1-12 (defaults to current month)

    Response format:
    {
      "year": 2023,
      "month": 5,
      "days": {
         "1": [{"id": 1, "title": "...", "date": "2023-05-01T10:00:00"}, ...],
         "15": [ ... ]
      }
    }
    """

    try:
        today = timezone.localtime(timezone.now())
        year = int(request.GET.get('year', today.year))
        month = int(request.GET.get('month', today.month))
    except Exception:
        return JsonResponse({"success": False, "error": "Invalid year or month"}, status=400)

    # clamp month/year to valid values
    if month < 1 or month > 12:
        return JsonResponse({"success": False, "error": "Month must be 1-12"}, status=400)

    events_qs = Event.objects.filter(date__year=year, date__month=month).order_by('date')

    days = {}
    for ev in events_qs:
        day = str(ev.date.day)
        days.setdefault(day, []).append({
            'id': ev.id,
            'title': ev.title,
            'date': ev.date.isoformat(),
            'start_time': ev.start_time.isoformat() if ev.start_time else None,
            'end_time': ev.end_time.isoformat() if ev.end_time else None,
            'location': ev.location,
        })

    resp = {
        'success': True,
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'days': days,
    }

    return JsonResponse(resp)