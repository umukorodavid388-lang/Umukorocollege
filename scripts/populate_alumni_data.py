"""
Script to populate initial alumni and campus data
Run with: python manage.py shell < scripts/populate_alumni_data.py
"""

from alumni.models import AlumniNetwork, Campus

# Create or update AlumniNetwork with institution founding year
network, created = AlumniNetwork.objects.get_or_create(pk=1)
if created:
    # Change founding_year to match your institution
    network.founding_year = 1960
    network.description = "Our institution has proudly educated leaders and innovators across the globe."
    network.save()
    print("✓ AlumniNetwork created with founding year: 1960")
else:
    print("✓ AlumniNetwork already exists")

# Create sample campuses (update these with your actual campuses)
campuses_data = [
    {
        'name': 'Main Campus',
        'country': 'United States',
        'city': 'New York',
        'address': '123 University Ave, New York, NY 10001'
    },
    {
        'name': 'International Campus',
        'country': 'United Kingdom',
        'city': 'London',
        'address': '456 Academic Way, London, UK'
    },
    {
        'name': 'Asia Pacific Campus',
        'country': 'Singapore',
        'city': 'Singapore',
        'address': '789 Education Plaza, Singapore'
    },
    {
        'name': 'Middle East Campus',
        'country': 'United Arab Emirates',
        'city': 'Dubai',
        'address': '321 Knowledge Hub, Dubai, UAE'
    },
    {
        'name': 'European Campus',
        'country': 'Germany',
        'city': 'Berlin',
        'address': '654 Scholar Street, Berlin, Germany'
    },
]

created_count = 0
for campus_data in campuses_data:
    campus, created = Campus.objects.get_or_create(
        name=campus_data['name'],
        defaults={
            'country': campus_data['country'],
            'city': campus_data['city'],
            'address': campus_data['address'],
            'is_active': True
        }
    )
    if created:
        created_count += 1
        print(f"✓ Created campus: {campus.name} ({campus.country})")
    else:
        print(f"• Campus already exists: {campus.name}")

print(f"\n✓ Total new campuses created: {created_count}")

# Display current statistics
network = AlumniNetwork.objects.first()
print(f"\n📊 Current Alumni Network Statistics:")
print(f"   - Total Alumni: {network.total_alumni_worldwide}")
print(f"   - Countries: {network.total_countries}")
print(f"   - Years of Excellence: {network.years_of_excellence}+")
print(f"   - Campuses: {network.total_campuses}")
