"""Result Task Admin interface."""

from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

try:
    ALLOW_EDITS = settings.DJANGO_CELERY_RESULTS['ALLOW_EDITS']
except (AttributeError, KeyError):
    ALLOW_EDITS = False
    pass

from django.contrib import admin
from .models import GroupResult, TaskResult


# @admin.register(TaskResult)
class TaskResultAdmin(admin.ModelAdmin):
    """Admin-interface for results of tasks."""

    model = TaskResult
    date_hierarchy = 'date_done'
    list_display = ('task_id', 'periodic_task_name', 'task_name', 'date_done',
                    'status', 'worker')
    list_filter = ('status', 'date_done', 'periodic_task_name', 'task_name',
                   'worker')
    readonly_fields = ('date_created', 'date_started', 'date_done',
                       'result', 'meta')
    search_fields = ('task_name', 'task_id', 'status', 'task_args',
                     'task_kwargs')
    fieldsets = (
        (None, {
            'fields': (
                'task_id',
                'task_name',
                'periodic_task_name',
                'status',
                'worker',
                'content_type',
                'content_encoding',
            ),
            'classes': ('extrapretty', 'wide')
        }),
        (_('Parameters'), {
            'fields': (
                'task_args',
                'task_kwargs',
            ),
            'classes': ('extrapretty', 'wide')
        }),
        (_('Result'), {
            'fields': (
                'result',
                'date_created',
                'date_started',
                'date_done',
                'traceback',
                'meta',
            ),
            'classes': ('extrapretty', 'wide')
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    # def get_readonly_fields(self, request, obj=None):
    #     if ALLOW_EDITS:
    #         return self.readonly_fields
    #     else:
    #         return list({
    #             field.name for field in self.opts.local_fields
    #         })


# admin.site.register(TaskResult, TaskResultAdmin)


class GroupResultAdmin(admin.ModelAdmin):
    """Admin-interface for results  of grouped tasks."""

    model = GroupResult
    date_hierarchy = 'date_done'
    list_display = ('group_id', 'date_done')
    list_filter = ('date_done',)
    readonly_fields = ('date_created', 'date_done', 'result')
    search_fields = ('group_id',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(GroupResult, GroupResultAdmin)
