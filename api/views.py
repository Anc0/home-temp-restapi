import json

from django.core.serializers import serialize
from django.http import HttpResponse

from api.helpers import TopicRetriever, TopicRecordRetriever
from api.helpers.interpolation import Interpolation


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


def records_for_topic_offset(request, topic_id, offset):
    # Get data from the database
    data = TopicRecordRetriever().get_records_for_topic(topic_id=topic_id, seconds_back=offset)
    # Interpolate missing ticks
    data = Interpolation(ticks=72).tick([{'created': x.created, 'value': x.value} for x in data])
    # Json serialize the results
    data = json.dumps(data, indent=4, sort_keys=True, default=str)
    # Return the respose
    return HttpResponse(data, content_type='application/json')
