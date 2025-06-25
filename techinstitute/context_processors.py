def notification_count(request):
    if request.user.is_authenticated:
        count = request.user.notifications.filter(is_read=False).count()
    else:
        count = 0
    return {'notification_count': count}


# techinstitute/context_processors.py
def notifications_processor(request):
    if request.user.is_authenticated:
        notifications = request.user.notifications.all().order_by('-created_at')
        unread_count = request.user.notifications.filter(is_read=False).count()
        return {
            'user_notifications': notifications,
            'notification_count': unread_count,
        }
    return {}

