from datetime import timedelta, datetime

import pytz

from api.models import Topic, TopicRecord


class TopicRetriever:

    def __init__(self):
        pass

    def get_all_topics(self):
        """
        Retrieve all topics (feasible for home use, where there is not a lot of topics).
        :return: list of all topics
        """
        return Topic.objects.all()

    def get_topics(self, topic_names):
        """
        Retrieve topics with name in topic_names list
        :param topic_names: [list[string]] topic names
        :return: list of topics
        """
        return Topic.objects.filter(name__in=topic_names)

    def get_topic(self, topic_name):
        """
        Retrieve a single topic with name
        :param topic_name: [string] name of the topic
        :return: Topic with name=topic_name
        """
        return Topic.objects.get(name=topic_name)


class TopicRecordRetriever:

    def __init__(self):
        self.topics = TopicRetriever()

    def get_records_for_topic(self, topic_name, from_time=datetime.now(pytz.UTC) - timedelta(hours=1),
                              to_time=datetime.now(pytz.UTC)):
        """
        Retrieve topic records for single topic between from and to time.
        :param topic_name: [string] name of the topic
        :param from_time: [datetime tz] start of the interval
        :param to_time: [datetime tz] end of the interval
        :return: topic records
        """
        return TopicRecord.objects.filter(topic=self.topics.get_topic(topic_name=topic_name), created__gte=from_time,
                                          created__lte=to_time)

    def get_records_for_topics(self, topic_names=[], from_time=datetime.now(pytz.UTC) - timedelta(hours=1),
                              to_time=datetime.now(pytz.UTC)):
        """
        Retrieve topic records for multiple topics between from and to time
        :param topic_name: [list[string]] list of topic names, if the list is empty, return for all topics
        :param from_time: [datetime tz] start of the interval
        :param to_time: [datetime tz] end of the interval
        :return: topic records
        """
        if not topic_names:
            topics =  self.topics.get_all_topics()
        else:
            topics = self.topics.get_topics(topic_names)

        return TopicRecord.objects.filter(topic__in=topics, created__gte=from_time, created__lte=to_time)
