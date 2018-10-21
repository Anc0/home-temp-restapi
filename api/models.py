from django.db import models, connection


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
        if not self.last_record or topic_record.created > self.last_record.created:
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

    def get_aggregated_data(self, topic_id, offset):
        time_slice = offset * 24 * 60 / 72
        sql = """SELECT 1 AS id, date_round(created, '{} minutes'::interval), AVG(Value)
                FROM api_topicrecord
                WHERE created >= current_timestamp - '{} day'::interval AND topic_id = {}
                GROUP BY date_round(created, '{} minutes'::interval)
                ORDER BY date_round(created, '{} minutes'::interval);""".format(time_slice, offset, topic_id, time_slice, time_slice)
        cursor = connection.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        return [{"created": x[1], "value": x[2]} for x in data]

    def __str__(self):
        return "TopicRecord: {}, value: {}, at: {}".format(self.topic.name, self.value, self.created)
