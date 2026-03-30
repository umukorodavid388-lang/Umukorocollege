from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import *
from academics.models import ProgramIntrest
# Create your views here.

def addmission(request):
    """Display admissions page with all information"""
    program_interests = ProgramIntrest.objects.all()
    tutionnote = TutionNote.objects.first()
    campus = CampusVisst.objects.first()
    campus_visit = CampusVisitContent.objects.all() if campus else []
    
    context = {
        'application_steps': ApplicationStep.objects.filter(is_active=True),
        'requirements': AdmissionRequirement.objects.filter(is_active=True),
        'tuition_programs': TuitionProgram.objects.filter(is_active=True),
        'deadlines': AdmissionDeadline.objects.filter(is_active=True),
        'program_interests': program_interests,
        'tutionnote':tutionnote,
        'campus': campus,
        'campus_visit': campus_visit,
    }
    return render(request, 'admissions/admissions.html', context)


@require_http_methods(["POST"])
def submit_information_request(request):
    """Handle information request form submission"""
    program_intre = InformationRequest.objects.all()
    try:
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        program_interest = request.POST.get('subject')
        message = request.POST.get('message', '')
        
        # Create information request
        # Try to get program by ID first, then by name
        program_obj = None
        if program_interest:
            try:
                program_obj = ProgramIntrest.objects.get(id=program_interest)
            except (ProgramIntrest.DoesNotExist, ValueError):
                # If ID lookup fails, try by name
                program_obj = ProgramIntrest.objects.filter(name=program_interest).first()
        InformationRequest.objects.create(
            name=name,
            email=email,
            phone=phone,
            program=program_obj,
            message=message,
            status='new'
        )
        
        messages.success(request, 'Your information request has been submitted successfully!')
        return redirect('addmission')
    
    except Exception as e:
        messages.error(request, f'Error submitting request: {str(e)}')
        return redirect('addmission')
    

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
        return redirect('addmission')
    
    except Exception as e:
        messages.error(request, f'Error submitting visit request: {str(e)}')
        return redirect('addmission')


def campus_visits(request):
    """List all campus visits (optional admin view)"""
    visits = CampusVisitRequest.objects.all().order_by('-created_at')
    context = {
        'visits': visits
    }
    return render(request, 'admissions/campus_visits.html', context)


def information_requests(request):
    """List all information requests (optional admin view)"""
    requests_list = InformationRequest.objects.all().order_by('-created_at')
    context = {
        'requests': requests_list
    }
    return render(request, 'admissions/information_requests.html', context)