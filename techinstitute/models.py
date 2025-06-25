from django.db import models
from django.contrib.auth.models import User
from courses.models import Course

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_reference = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications'  # This line is the key fix
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    url = models.URLField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


    class Meta:
        ordering = ['-created_at']