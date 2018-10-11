from api.models import Topic


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