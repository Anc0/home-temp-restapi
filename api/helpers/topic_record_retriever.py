from datetime import datetime, timedelta

import pytz

from api.helpers.topic_retriever import TopicRetriever
from api.models import TopicRecord


class TopicRecordRetriever:

    def __init__(self):
        self.topics = TopicRetriever()

    def get_records_for_topic(self, topic_id, seconds_back=3600):
        """
        Retrieve topic records for single topic between from and to time.
        :param topic_id: [int] topic id
        :param seconds_back: off set of starting time of the data
        :return: topic records
        """
        topic = self.topics.get_topic(id=topic_id)[0]
        data = list(TopicRecord.objects.filter(topic=topic.id,
                                               created__range=(datetime.now(pytz.UTC) -
                                                               timedelta(seconds=seconds_back),
                                                               datetime.now(pytz.UTC))))
        for x in data:
            x.value += topic.temperature_offset
        return data

    def get_records_for_topics(self, topic_names=None, from_time=datetime.now(pytz.UTC) - timedelta(hours=1),
                               to_time=datetime.now(pytz.UTC)):
        """
        Retrieve topic records for multiple topics between from and to time
        :param topic_names: [list[string]] list of topic names, if the list is empty, return for all topics
        :param from_time: [datetime tz] start of the interval
        :param to_time: [datetime tz] end of the interval
        :return: topic records
        """
        if not topic_names:
            topics =  self.topics.get_all_topics()
        else:
            topics = self.topics.get_topics(topic_names)

        return TopicRecord.objects.filter(topic__in=topics, created__gte=from_time, created__lte=to_time)