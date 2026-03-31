import statistics
from django.shortcuts import render, redirect
from django.utils import timezone
from website.models import *
from academics.models import *
from news.models import *
from eventlife.models import *
from faculty.models import *
from django.views.decorators.http import require_http_methods
from django.contrib import messages

def Index(request):
    hero = Hero.objects.first()
    features = hero.features.all() if hero else []
    upcoming_event = getattr(hero, 'upcoming_event', None)
    about = About.objects.first()
    timeline_items = about.timeline_items.all() if about else []
    core_values = about.core_values.all() if about else []
    # Students Life content
    students_life = None
    students_activities = []
    try:
        from website.models import StudentsLife
        students_life = StudentsLife.objects.first()
        students_activities = students_life.activities.all() if students_life else []
    except Exception:
        students_life = None
        students_activities = []
    
    # Get featured programs
    featured_program = Program.objects.filter(is_featured=True).first()
    programs = Program.objects.filter(is_featured=False)
    new = News.objects.all() 
    
    # Get upcoming events with likes and shares data
    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:3]
    events = events.prefetch_related('likes', 'shares')
    
    # Get testimonials
    testimonials = Testimonial.objects.filter(is_active=True).order_by('order')
    
    # Get statistics
    stats = Statistic.objects.first()
    if not stats:
        stats = Statistic.objects.create()

    context = {
        'hero': hero,
        'features': features,
        'upcoming_event': upcoming_event,
        'about': about,
        'timeline_items': timeline_items,
        'core_values': core_values,
        'featured_program': featured_program,
        'testimonials': testimonials,
        'programs': programs,
        'students_life': students_life,
        'students_activities': students_activities,
        'new': new,
        'events': events,
        'stats': stats,
    }
    return render(request, 'website/index.html', context)



def about(request):
    abouts = About.objects.first()
    timeline_items = abouts.timeline_items.all() if abouts else []
    core_values = abouts.core_values.all() if abouts else []

    # staff
    staff = Staff.objects.all()

    # leadership
    leader = leadership.objects.first()
    icon = Icon.objects.all() if leader else []



    context ={
       'abouts': abouts,
        'timeline_items': timeline_items,
        'core_values': core_values,
        'staff':staff,
        'leader':leader,
        'icon':icon,
    }
    return render(request, 'website/about.html', context)



def students_life(request):
    student_life_intro = StudentLifeIntro.objects.filter(is_active=True).first()
    student_organizations = StudentOrganization.objects.filter(is_active=True).order_by('order')
    athletics_programs = AthleticsProgram.objects.filter(is_active=True).order_by('order')[:4]
    campus_facilities = StudentLifeFacility.objects.filter(is_active=True).order_by('order')[:4]
    support_services = StudentSupportService.objects.filter(is_active=True).order_by('order')[:3]
    gallery_images = StudentLifeGalleryImage.objects.filter(is_active=True).order_by('order')
    
    context = {
        'student_life_intro': student_life_intro,
        'student_organizations': student_organizations,
        'athletics_programs': athletics_programs,
        'campus_facilities': campus_facilities,
        'support_services': support_services,
        'gallery_images': gallery_images,
    }
    return render(request, 'website/students-life.html', context)


def contect(request):
    return render(request, 'website/contact.html')



@require_http_methods(["POST"])
def submit_campus_visit_request(request):
    """Handle campus visit booking request"""
    try:
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        preferred_date = request.POST.get('preferred_date')
        preferred_time = request.POST.get('preferred_time')
        visit_type = request.POST.get('visit_type', 'in_person')
        number_of_visitors = request.POST.get('number_of_visitors', 1)
        special_requests = request.POST.get('special_requests', '')
        
        # Create campus visit request
        CampusVisitRequest.objects.create(
            name=name,
            email=email,
            phone=phone,
            preferred_date=preferred_date,
            preferred_time=preferred_time,
            visit_type=visit_type,
            number_of_visitors=int(number_of_visitors),
            special_requests=special_requests,
            is_confirmed=False
        )
        
        messages.success(request, 'Your campus visit request has been submitted successfully!')
        return redirect('students_life')
    
    except Exception as e:
        messages.error(request, f'Error submitting visit request: {str(e)}')
        return redirect('students_life')
    

def alumni(request):
    from alumni.models import AlumniSuccess, AlumniNetwork
    from eventlife.models import EventCategory
    
    # Find (or create) the category corresponding to alumni events
    alumni_category = EventCategory.objects.filter(text__iexact='alumni').first()

    # Get upcoming events that are featured, in the future, **and** belong to the alumni category
    if alumni_category:
        upcoming_events = Event.objects.filter(
            featured=True,
            date__gte=timezone.now().date(),
            eventcategories=alumni_category
        ).order_by('date')[:2]
    else:
        # if the alumni category doesn't exist yet, avoid returning unrelated events
        upcoming_events = Event.objects.none()
    
    # Get alumni success stories
    success_stories = AlumniSuccess.objects.filter(is_featured=True).order_by('order')[:3]
    
    # Get alumni network statistics
    network_stats = AlumniNetwork.objects.first()
    if not network_stats:
        network_stats = AlumniNetwork.objects.create()
    
    context = {
        'upcoming_events': upcoming_events,
        'success_stories': success_stories,
        'network_stats': network_stats,
    }
    return render(request, 'website/alumni.html', context)



def privacy(request):
    from website.models import PrivacyPolicy
    privacy_policy = PrivacyPolicy.objects.filter(is_active=True).first() or PrivacyPolicy.objects.first()

    context = {
        'privacy_policy': privacy_policy,
    }
    return render(request, 'website/privacy.html', context)


def term_services(request):
    return render(request, 'website/terms-of-service.html')


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)


def custom_500(request):
    return render(request, '500.html', status=500)


