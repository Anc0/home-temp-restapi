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
        return Topic.objects.filter(display=True)

    def get_topics(self, topic_names):
        """
        Retrieve topics with name in topic_names list
        :param topic_names: [list[string]] topic names
        :return: list of topics
        """
        return Topic.objects.filter(name__in=topic_names)

    def get_topic(self, id=None, name=None):
        """
        Retrieve a single topic with name
        :param topic_name: [string] name of the topic
        :return: Topic with name=topic_name
        """
        if not id and not name:
            raise Exception("You have to set either topic name or topic id.")
        if not id:
            return Topic.objects.filter(name=name)
        if not name:
            return Topic.objects.filter(id=id)
        return Topic.objects.filter(id=id, name=name)


class TopicRecordRetriever:

    def __init__(self):
        self.topics = TopicRetriever()

    def get_records_for_topic(self, topic_id, from_time=datetime.now(pytz.UTC) - timedelta(hours=1),
                              to_time=datetime.now(pytz.UTC), seconds_back=0):
        """
        Retrieve topic records for single topic between from and to time.
        :param topic_name: [string] name of the topic
        :param from_time: [datetime tz] start of the interval
        :param to_time: [datetime tz] end of the interval
        :param seconds_back: off set of starting time of the data (used instead of datetime range if set)
        :return: topic records
        """
        if seconds_back > 0:
            return TopicRecord.objects.filter(topic=self.topics.get_topic(id=topic_id)[0],
                                              created__range=(datetime.now(pytz.UTC) - timedelta(seconds=seconds_back),
                                                              datetime.now(pytz.UTC)))
        else:
            return TopicRecord.objects.filter(topic=self.topics.get_topic(id=topic_id)[0],
                                              created__range=(from_time, to_time))

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
