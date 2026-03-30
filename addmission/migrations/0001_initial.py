# Generated migration for addmission app

from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('academics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgramIntrest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StudentRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pics', models.ImageField(upload_to='media/addmission/')),
                ('student_name', models.CharField(max_length=200)),
                ('student_email', models.EmailField(max_length=254, unique=True)),
                ('student_phone', models.CharField(blank=True, max_length=20)),
                ('enrollment_date', models.DateField(auto_now_add=True)),
                ('completion_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('enrolled', 'Enrolled'), ('completed', 'Completed'), ('dropped', 'Dropped'), ('suspended', 'Suspended')], default='enrolled', max_length=20)),
                ('is_passed', models.BooleanField(default=False, help_text='Check if student completed successfully')),
                ('grades', models.CharField(blank=True, help_text='e.g., A, B, C, D, F', max_length=5)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='academics.program')),
            ],
            options={
                'ordering': ['-enrollment_date'],
            },
        ),
        migrations.CreateModel(
            name='TuitionProgram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tuition_per_year', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fees', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True)),
                ('finicial', models.CharField(max_length=200)),
                ('details', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('program_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='program_interest', to='addmission.programintrest')),
            ],
        ),
        migrations.CreateModel(
            name='InformationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('message', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('new', 'New'), ('contacted', 'Contacted'), ('converted', 'Converted'), ('rejected', 'Rejected')], default='new', max_length=20)),
                ('is_contacted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='program', to='addmission.programintrest')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CampusVisitRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('preferred_date', models.DateField()),
                ('preferred_time', models.TimeField()),
                ('visit_type', models.CharField(choices=[('in_person', 'In-Person Tour'), ('virtual', 'Virtual Tour')], default='in_person', max_length=20)),
                ('number_of_visitors', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('special_requests', models.TextField(blank=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ApplicationStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_number', models.IntegerField(unique=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['step_number'],
            },
        ),
        migrations.CreateModel(
            name='AdmissionRequirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requirement', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('note', models.TextField(blank=True)),
                ('is_mandatory', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='AdmissionDeadline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deadline_name', models.CharField(max_length=100)),
                ('deadline_date', models.DateField()),
                ('description', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['order', 'deadline_date'],
            },
        ),
        migrations.AddConstraint(
            model_name='studentregistration',
            constraint=models.UniqueConstraint(fields=('program', 'student_email'), name='unique_program_student_email'),
        ),
    ]
