from django.utils import timezone

def server_time(request):
    """Adds the current server time (ISO formatted) to the template context."""
    return {'server_now': timezone.now().isoformat()}

def user_roles(request):
    """Adds user role information to the template context."""
    is_manager = False
    if request.user.is_authenticated:
        is_manager = request.user.is_superuser or request.user.groups.filter(name='Managers').exists()
    return {
        'is_manager': is_manager,
    }