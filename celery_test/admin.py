from django.contrib import admin

from .models import Counter


class CounterAdmin(admin.ModelAdmin):
    list_display = ('id', 'value')


admin.site.register(Counter, CounterAdmin)
