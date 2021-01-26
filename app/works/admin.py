from django.contrib import admin

from works.models import Work


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    ordering = ['-id']
    list_display = ['user', 'title', 'created_at', 'status']
    readonly_fields = ['status']
