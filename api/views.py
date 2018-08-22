import json

from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse

from api.helpers import TopicRetriever, TopicRecordRetriever


def index(request):
    return HttpResponse("Hello world, this is temp rest api")


def topics(request):
    data = serialize('json', TopicRetriever().get_all_topics())
    return HttpResponse(data, content_type="application/json")


def topic(request, topic_id):
    data = serialize('json', TopicRetriever().get_topic(id=topic_id))
    return HttpResponse(data, content_type='application/json')

def records_for_topic(request, topic_id):
    data = serialize('json', TopicRecordRetriever().get_records_for_topic(topic_id=topic_id))
    return HttpResponse(data, content_type='application/json')
