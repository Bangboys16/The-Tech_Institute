# admin.py
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from .models import Notification, Payment

from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from .models import Notification, Payment

class NotificationAdminForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(payment__verified=True).distinct(),
        required=True,
        widget=forms.SelectMultiple,
        label="Send to Users"
    )

    class Meta:
        model = Notification
        fields = ['title', 'message', 'url', 'users']

    def save(self, commit=True):
        # Prevent saving the main instance
        return super().save(commit=False)



   
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    form = NotificationAdminForm
    exclude = ['user']

    def save_model(self, request, obj, form, change):
        # Prevent default save by not saving `obj`
        users = form.cleaned_data['users']
        for user in users:
            Notification.objects.create(
                user=user,
                title=form.cleaned_data['title'],
                message=form.cleaned_data['message'],
                url=form.cleaned_data['url']
            )

    def save_formset(self, request, form, formset, change):
        # Prevent saving related inlines if any
        pass
