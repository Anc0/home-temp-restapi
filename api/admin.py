from django.contrib import admin

from .models import Topic, TopicRecord


class TopicAdmin(admin.ModelAdmin):
        fields = ['name', 'short_name', 'display', 'temperature_offset']


admin.site.register(TopicRecord)
admin.site.register(Topic, TopicAdmin)
