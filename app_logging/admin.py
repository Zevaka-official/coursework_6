from django.contrib import admin
from django.db.models import Count

from app_logging.models import MailingReport


class IsGroupReportFilter(admin.SimpleListFilter):
    title = 'Групповой отчет'
    parameter_name = 'child_count'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Да'),
            ('No', 'Нет')
        )

    def queryset(self, request, queryset):
        value = self.value()

        match value:
            case 'Yes':
                return queryset.filter(child_count__gt=0)
            case 'No':
                return queryset.filter(child_count=0)
            case _:
                return queryset


class ChildReportsInline(admin.TabularInline):
    model = MailingReport
    can_delete = False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False


@admin.register(MailingReport)
class MailingReportAdmin(admin.ModelAdmin):
    list_display = ['report_status', 'report_date_time', 'mailing']
    list_filter = ['report_status', IsGroupReportFilter]
    search_fields = ['report_date_time', 'report_message']
    inlines = [
        ChildReportsInline
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(child_count=Count('child_reports'))

    def child_count(self, inst):
        return inst.child_count

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False
