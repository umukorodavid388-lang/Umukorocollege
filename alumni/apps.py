from django.apps import AppConfig


class AlumniConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'alumni'
    
    def ready(self):
        """Register signals when app is ready"""
        import alumni.signals
