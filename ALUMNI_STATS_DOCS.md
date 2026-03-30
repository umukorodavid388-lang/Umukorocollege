# Alumni Network Statistics - Dynamic System Documentation

## Overview

The Alumni Network statistics are now **fully dynamic** and automatically update based on actual data in your database. Three main metrics are calculated automatically:

1. **Total Alumni Worldwide** - Count of students who have completed their programs
2. **Countries** - Number of countries where your campuses are located
3. **Years of Excellence** - Calculated from your institution's founding year

---

## How It Works

### 1. Total Alumni Worldwide
- **Source**: `StudentRegistration` model  
- **Logic**: Counts all students with:
  - `status = 'completed'` 
  - `is_passed = True`
- **Updates**: Automatically whenever a student record is marked as completed
- **Formula**: 
  ```python
  AlumniNetwork.total_alumni_worldwide
  # Returns: Count of all graduated students
  ```

### 2. Countries with Campuses
- **Source**: `Campus` model
- **Logic**: Counts distinct countries where active campuses are located
- **Updates**: Automatically when campuses are added/removed/deactivated
- **Formula**:
  ```python
  AlumniNetwork.total_countries
  # Returns: Distinct country count from active campuses
  ```

### 3. Years of Excellence
- **Source**: `AlumniNetwork.founding_year` field
- **Logic**: Current year minus founding year
- **Updates**: Automatically recalculated each year
- **Formula**:
  ```python
  AlumniNetwork.years_of_excellence
  # Returns: datetime.now().year - founding_year
  ```

---

## Setup Instructions

### 1. Configure Founding Year
Go to Django Admin → Alumni → Alumni Network

- Set the **Founding Year** (e.g., 1960)
- Add a **Description** of your institution
- The years of excellence will auto-calculate

### 2. Add Campuses
Go to Django Admin → Alumni → Campuses

Add all your institution's campuses:
- **Name**: Faculty of Arts, Main Campus, etc.
- **Country**: Full country name
- **City**: City name
- **Address**: Full address
- **Active**: Check to include in country count

**Example**:
```
Name: Main Campus
Country: United States
City: New York
Address: 123 University Ave, New York, NY 10001
Active: ✓
```

### 3. Mark Students as Graduated
In the Admissions app → Student Registration, update student records:
- Set **Status** to "Completed"
- Check "Is Passed" if successful
- Set **Completion Date** (optional)

Only students with both `status='completed'` AND `is_passed=True` count as alumni.

---

## Example Setup

### Initial Configuration
```
Founding Year: 1960
Current Year: 2026
Years of Excellence: 66+
```

### Campus Data
```
Main Campus (USA)
London Campus (UK)
Singapore Campus (Singapore)
Dubai Campus (UAE)
Berlin Campus (Germany)
```
↓ Results in:
- **Countries: 5** (USA, UK, Singapore, UAE, Germany)

### Student Data
```
200 students with status=completed AND is_passed=True
```
↓ Results in:
- **Alumni Worldwide: 200**

---

## Admin Display

The Alumni Network admin page shows:
- ✓ Total Alumni (auto-calculated from student registrations)
- ✓ Countries (auto-calculated from active campuses)
- ✓ Years of Excellence (auto-calculated from founding year)
- ✓ Total Campuses (auto-calculated from campus count)

All values refresh in real-time when you modify data.

---

## Template Integration

The alumni page displays the stats automatically:

```django
{% if network_stats %}
  {{ network_stats.total_alumni_worldwide }}  <!-- Auto-calculated count -->
  {{ network_stats.total_countries }}         <!-- Auto-calculated count -->
  {{ network_stats.years_of_excellence }}+    <!-- Auto-calculated count -->
{% endif %}
```

No manual updates needed—the stats update whenever:
- A student is marked as completed/graduated
- A campus is added, removed, or deactivated
- The founding year is changed

---

## API Reference

### AlumniNetwork Model

```python
from alumni.models import AlumniNetwork

network = AlumniNetwork.objects.first()

# Properties (auto-calculated)
network.total_alumni_worldwide    # int: Count of completed students
network.total_countries           # int: Count of unique campus countries
network.years_of_excellence       # int: Years since founding
network.total_campuses            # int: Count of active campuses

# Fields
network.founding_year             # int: Year institution was founded
network.description               # str: Institution description
```

### Campus Model

```python
from alumni.models import Campus

# Add a campus
Campus.objects.create(
    name="New York Campus",
    country="United States",
    city="New York",
    address="123 University Ave, NY 10001",
    is_active=True
)

# Query campuses by country
campuses = Campus.objects.filter(country="Singapore", is_active=True)
```

---

## Troubleshooting

**Issue**: Alumni count shows 0 despite having students
- **Solution**: Check that students in `StudentRegistration` have:
  - `status = 'completed'`
  - `is_passed = True`

**Issue**: Countries count is incorrect
- **Solution**: Check that campuses have:
  - `is_active = True`
  - Correct country names (must match exactly)

**Issue**: Years of Excellence is wrong
- **Solution**: Verify the `founding_year` in Alumni Network admin

---

## Customization

### Change Founding Year
1. Go to Admin → Alumni → Alumni Network
2. Update "Founding Year"
3. Save - Years of Excellence auto-updates

### Add/Remove Campuses
1. Go to Admin → Alumni → Campuses  
2. Add new or edit existing
3. Toggle "Active" to include/exclude from country count

### Modify Alumni Requirements
To change what counts as an alumnus, edit the property in [alumni/models.py](alumni/models.py):

```python
@property
def total_alumni_worldwide(self):
    from addmission.models import StudentRegistration
    return StudentRegistration.objects.filter(
        status='completed',
        is_passed=True
    ).count()
```

---

## Notes

- All calculations are real-time properties
- No manual data entry needed for statistics
- Falls back to defaults if no data exists
- Works with the existing student registration system
