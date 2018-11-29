from django.contrib import admin

from .models import Counter, VisitLog


class CounterAdmin(admin.ModelAdmin):
    list_display = ('id', 'value')


class VisitLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'method', 'path', 'query', 'ip', 'response_code', 'response_length', 'created_at')
    ordering = ('-id',)


admin.site.register(Counter, CounterAdmin)
admin.site.register(VisitLog, VisitLogAdmin)
