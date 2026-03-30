from django.shortcuts import render
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
def faculty_home(request):
    staff_categorys = StaffCategory.objects.all()
    staff_members = Staff.objects.all() 
    query = request.GET.get('q')
    if query:
        staff_members = staff_members.filter(
            Q(name__icontains=query) |
            Q(work_tile__icontains=query) 
        ) 

    paginator = Paginator(staff_members, 9)  # 9 faculty per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)



    context = {     
        'staff_categorys': staff_categorys,
        'staff_members': staff_members, 
        'query': query,
        'page_obj': page_obj,
    }  
    return render(request, 'faculty/faculty-staff.html', context)