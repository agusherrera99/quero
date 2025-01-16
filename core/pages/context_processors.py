# context_processors.py
from account.models import Notification

def notification_count(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        notification_count = notifications.count()
    else:
        notifications = []  # Define an empty list for unauthenticated users
        notification_count = 0

    return {
        'notifications': notifications,
        'notification_count': notification_count
    }

