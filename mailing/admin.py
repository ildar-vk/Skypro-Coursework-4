from django.contrib import admin

from .models import Client, Mailing, MailingAttempt, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "owner")
    search_fields = ("full_name", "email")
    list_filter = ("owner",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("theme", "owner")
    search_fields = ("theme",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "start_time", "end_time", "status", "message", "owner")
    list_filter = ("status", "start_time", "owner")
    search_fields = ("message__theme",)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ("attempt_time", "status", "mailing")
    list_filter = ("status",)
