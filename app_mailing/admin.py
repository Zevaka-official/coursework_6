from django.contrib import admin
from django.db.models import Count

from app_mailing.models import MailMessage, Mailing, MailingResend


class MailingInline(admin.TabularInline):
    model = Mailing
    readonly_fields = ['id']
    extra = 1
    can_delete = True


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ['message', 'date_start', 'periodicity', 'mailing_status']
    list_filter = ['periodicity', 'mailing_status', 'message']


@admin.register(MailMessage)
class MailMessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'author', 'mailings_count']
    search_fields = ['subject', 'text']
    inlines = [
        MailingInline
    ]

    def mailings_count(self, obj):
        return obj.mailings_count

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(mailings_count=Count('mailings'))
        return queryset


@admin.register(MailingResend)
class MailingResendAdmin(admin.ModelAdmin):
    list_display = ['mailing', 'recipient', 'attempts_left']
    readonly_fields = ['mailing', 'recipient']
