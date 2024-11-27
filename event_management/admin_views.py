from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from event_management.models import Event
from user_management.models import CustomUser
from django.utils.timezone import now

@staff_member_required
def admin_report(request):
    """
    Generate an admin report summarizing platform statistics.
    """
    # Fetching data for the report
    total_users = CustomUser.objects.count()
    total_events = Event.objects.count()
    active_events = Event.objects.filter(date__gte=now().date()).count()  # Active events with upcoming dates
    top_users_by_points = CustomUser.objects.order_by('-total_points')[:10]  # Top 10 users by points

    context = {
        'total_users': total_users,
        'total_events': total_events,
        'active_events': active_events,
        'top_users_by_points': top_users_by_points,
    }

    # Render the report template
    return render(request, 'admin/admin_report.html', context)
