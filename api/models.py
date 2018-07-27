from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=255)

    last_record = models.OneToOneField('api.TopicRecord', null=True, on_delete=models.SET_NULL, related_name='last_record')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


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
