from django.contrib import admin
from djcelery.models import TaskMeta, TaskSetMeta

from .models import Counter


class CounterAdmin(admin.ModelAdmin):
    list_display = ('id', 'value')


admin.site.register(Counter, CounterAdmin)


class TaskMetaAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_id', 'status', 'result', 'date_done')
    readonly_fields = ('id', 'task_id', 'status', 'result', 'date_done', 'traceback', 'hidden', 'meta')


class TaskSetMetaAdmin(admin.ModelAdmin):
    list_display = ('id', 'taskset_id', 'result', 'date_done')
    readonly_fields = ('id', 'taskset_id', 'result', 'date_done', 'hidden')


admin.site.register(TaskMeta, TaskMetaAdmin)
admin.site.register(TaskSetMeta, TaskSetMetaAdmin)
