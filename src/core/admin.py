"""App for base admin classes."""
from allauth.account.models import EmailAddress
from django.contrib.auth.models import Group
from django_celery_beat.admin import PeriodicTaskForm
from django_celery_beat.utils import is_database_scheduler
from django_celery_results.admin import ALLOW_EDITS
from django_celery_results.models import GroupResult, TaskResult

from src.core.admins.base import BaseAdmin
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule, PeriodicTasks,
)
from celery import current_app
from django.conf import settings
from django.contrib import admin, messages
from django.db.models import Case, Value, When
from django.template.defaultfilters import pluralize
from django.utils.translation import gettext_lazy as _
from kombu.utils.json import loads

# re-register django-celery-beat
admin.site.unregister(Group)
admin.site.unregister(EmailAddress)
admin.site.unregister(TaskResult)
admin.site.unregister(GroupResult)
admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)


@admin.register(PeriodicTask)
class PeriodicTaskAdmin(BaseAdmin):
    """Admin class for PeriodicTask."""

    form = PeriodicTaskForm
    model = PeriodicTask
    celery_app = current_app
    date_hierarchy = 'start_time'
    list_display = ('name', 'enabled', 'scheduler', 'interval', 'start_time',
                    'last_run_at', 'one_off')
    list_filter = ['enabled', 'one_off', 'task', 'start_time', 'last_run_at']
    actions = ('enable_tasks', 'disable_tasks', 'toggle_tasks', 'run_tasks')
    search_fields = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'regtask', 'task', 'enabled', 'description',),
            'classes': ('extrapretty', 'wide'),
        }),
        (_('Schedule'), {
            'fields': ('interval', 'crontab', 'crontab_translation', 'solar',
                       'clocked', 'start_time', 'last_run_at', 'one_off'),
            'classes': ('extrapretty', 'wide'),
        }),
        (_('Arguments'), {
            'fields': ('args', 'kwargs'),
            'classes': ('extrapretty', 'wide', 'collapse', 'in'),
        }),
        (_('Execution Options'), {
            'fields': ('expires', 'expire_seconds', 'queue', 'exchange',
                       'routing_key', 'priority', 'headers'),
            'classes': ('extrapretty', 'wide', 'collapse', 'in'),
        }),
    )
    readonly_fields = (
        'last_run_at', 'crontab_translation',
    )

    def crontab_translation(self, obj):
        """Get human readable crontab."""
        return obj.crontab.human_readable

    change_form_template = 'admin/djcelery/change_periodictask_form.html'

    def changeform_view(self, request, object_id=None, form_url='',
                        extra_context=None):
        """Change form view."""
        extra_context = extra_context or {}
        crontabs = CrontabSchedule.objects.all()
        crontab_dict = {}
        for crontab in crontabs:
            crontab_dict[crontab.id] = crontab.human_readable
        extra_context["readable_crontabs"] = crontab_dict  # noqa
        return super().changeform_view(request, object_id,
                                       extra_context=extra_context)

    def changelist_view(self, request, extra_context=None):
        """Change list view."""
        extra_context = extra_context or {}
        scheduler = getattr(settings, 'CELERY_BEAT_SCHEDULER', None)
        extra_context["wrong_scheduler"] = not is_database_scheduler(scheduler)  # noqa
        return super().changelist_view(
            request, extra_context)

    def get_queryset(self, request):
        """Get queryset."""
        qs = super().get_queryset(request)
        return qs.select_related('interval', 'crontab', 'solar', 'clocked')

    def _message_user_about_update(self, request, rows_updated, verb):
        """Send message about action to user.

        `verb` should shortly describe what have changed (e.g. 'enabled').
        """
        self.message_user(
            request,
            _('{0} task{1} {2} successfully {3}').format(
                rows_updated,
                pluralize(rows_updated),
                pluralize(rows_updated, _('was,were')),
                verb,
            ),
        )

    @admin.action(
        description=_('Enable selected tasks')
    )
    def enable_tasks(self, request, queryset):
        """Enable selected tasks."""
        rows_updated = queryset.update(enabled=True)
        PeriodicTasks.update_changed()
        self._message_user_about_update(request, rows_updated, 'enabled')

    @admin.action(
        description=_('Disable selected tasks')
    )
    def disable_tasks(self, request, queryset):
        """Disable selected tasks."""
        rows_updated = queryset.update(enabled=False, last_run_at=None)
        PeriodicTasks.update_changed()
        self._message_user_about_update(request, rows_updated, 'disabled')

    @staticmethod
    def _toggle_tasks_activity(queryset):
        """Toggle activity of tasks."""
        return queryset.update(enabled=Case(
            When(enabled=True, then=Value(False)),
            default=Value(True),
        ))

    @admin.action(
        description=_('Toggle activity of selected tasks')
    )
    def toggle_tasks(self, request, queryset):
        rows_updated = self._toggle_tasks_activity(queryset)
        PeriodicTasks.update_changed()
        self._message_user_about_update(request, rows_updated, 'toggled')

    @admin.action(
        description=_('Run selected tasks')
    )
    def run_tasks(self, request, queryset):
        self.celery_app.loader.import_default_modules()
        tasks = [(self.celery_app.tasks.get(task.task),
                  loads(task.args),
                  loads(task.kwargs),
                  task.queue,
                  task.name)
                 for task in queryset]

        if any(t[0] is None for t in tasks):
            for i, t in enumerate(tasks):
                if t[0] is None:
                    break

            # variable "i" will be set because a list "tasks" is not empty
            not_found_task_name = queryset[i].task  # noqa

            self.message_user(
                request,
                _(f'task "{not_found_task_name}" not found'),
                level=messages.ERROR,
            )
            return

        task_ids = [
            task.apply_async(args=args, kwargs=kwargs, queue=queue,
                             periodic_task_name=periodic_task_name)
            if queue and len(queue)
            else task.apply_async(args=args, kwargs=kwargs,
                                  periodic_task_name=periodic_task_name)
            for task, args, kwargs, queue, periodic_task_name in tasks
        ]
        tasks_run = len(task_ids)
        self.message_user(
            request,
            _('{0} task{1} {2} successfully run').format(
                tasks_run,
                pluralize(tasks_run),
                pluralize(tasks_run, _('was,were')),
            ),
        )


@admin.register(CrontabSchedule)
class CrontabScheduleAdmin(BaseAdmin):
    """Admin class for CrontabSchedule."""

    list_display = ('__str__', 'human_readable')


@admin.register(TaskResult)
class TaskResultAdmin(BaseAdmin):
    """Admin class for TaskResult."""

    model = TaskResult
    date_hierarchy = 'date_done'
    list_display = ('task_id', 'periodic_task_name', 'task_name', 'date_done',
                    'status', 'worker')
    list_filter = ('status', 'date_done', 'periodic_task_name', 'task_name',
                   'worker')
    readonly_fields = ('date_created', 'date_done', 'result', 'meta')
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
                'date_done',
                'traceback',
                'meta',
            ),
            'classes': ('extrapretty', 'wide')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if ALLOW_EDITS:
            return self.readonly_fields
        else:
            return list({
                field.name for field in self.opts.local_fields
            })
