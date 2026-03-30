from django.contrib import messages
from urllib import request
from django.shortcuts import redirect, render
from faculty.models import *
from addmission.models import *
from django.views.decorators.http import require_http_methods
from addmission.models import InformationRequest
from .models import *

# Create your views here.
def academics(request):
    programs = Program.objects.filter(is_featured=False)[0:6]
    progra = programs.count()
    faculty_members = Staff.objects.all()
    program_intrests = ProgramIntrest.objects.all()


    context = { 
        'programs': programs,
        'faculty_members': faculty_members,
        'program_intrests': program_intrests,
        'progra':progra,
    } 
    return render(request, 'academics/academics.html', context)


@require_http_methods(["POST"])
def submit_information(request):
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
        return redirect('academics')
    
    except Exception as e:
        messages.error(request, f'Error submitting request: {str(e)}')
        return redirect('academics')
    

def program(request):
    programs = Program.objects.filter(is_featured=False)
    progra = programs.count()
    faculty_members = Staff.objects.all()
    program_intrests = ProgramIntrest.objects.all()


    context = {
        'programs': programs,
        'faculty_members': faculty_members,
        'program_intrests': program_intrests,
        'progra':progra,
    } 
    return render(request, 'academics/program.html', context)