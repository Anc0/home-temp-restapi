from django.contrib import admin

from .models import Topic, TopicRecord

admin.site.register(TopicRecord)


class TopicAdmin(admin.ModelAdmin):
        fields = ['name', 'short_name', 'display']


admin.site.register(Topic, TopicAdmin)
