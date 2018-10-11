from django.db import models


class Topic(models.Model):
    # Actual mqtt topic name
    name = models.CharField(max_length=255, unique=True)
    # User friendly displayed name
    short_name = models.CharField(max_length=255, default="Unnamed topic")

    temperature_offset = models.FloatField(default=0)

    last_record = models.OneToOneField('api.TopicRecord', null=True, on_delete=models.SET_NULL, related_name='last_record')

    # Should the topic be displayed in the webapp
    display = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def set_last_record(self, topic_record):
        if self.last_record is None or topic_record.created > self.last_record.created:
            self.last_record = topic_record
            self.save()

    def __str__(self):
        return "Topic: {}".format(self.name)


class TopicRecord(models.Model):

    CELSIUS = 'CE'
    FAHRENHEIT = 'FA'
    KELVIN = 'KE'

    UNITS = (
        (CELSIUS, 'Degrees celsius'),
        (FAHRENHEIT, 'Degrees fahrenheit'),
        (KELVIN, 'Degrees kelvin')
    )

    value = models.FloatField()
    units = models.CharField(max_length=2, default=CELSIUS, choices=UNITS)

    topic = models.ForeignKey('api.Topic', on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "TopicRecord: {}, value: {}, at: {}".format(self.topic.name, self.value, self.created)
