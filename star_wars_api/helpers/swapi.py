import requests
import json
import six
from urllib.parse import quote_plus

BASE_URL = 'http://swapi.co/api'
PLANETS = 'planets'


class ResourceDoesNotExist(Exception):
    pass


def query(query):
    headers = {'User-Agent': 'swapi-python'}
    response = requests.get(query, headers=headers)
    if response.status_code != 200:
        raise ResourceDoesNotExist('Resource does not exist')
    return response


class BaseModel(object):

    def __init__(self, raw_data):
        json_data = json.loads(raw_data)
        for key, value in six.iteritems(json_data):
            setattr(self, key, value)


class BaseQuerySet(object):

    def __init__(self):
        self.items = []

    def order_by(self, order_attribute):
        ''' Return the list of items in a certain order '''
        to_return = []
        for f in sorted(self.items, key=lambda i: getattr(i, order_attribute)):
            to_return.append(f)
        return to_return

    def count(self):
        ''' Get the number of items in this queryset'''
        return len(self.items)

    def iter(self):
        ''' A generator that returns each resource in self.items '''
        for i in self.items:
            yield i


class PlanetQuerySet(BaseQuerySet):

    def __init__(self, list_of_urls):
        super(PlanetQuerySet, self).__init__()
        for url in list_of_urls:
            response = query(url)
            self.items.append(Planet(response.content))

    def __repr__(self):
        return '<PlanetQuerySet - {0}>'.format(str(len(self.items)))


class Planet(BaseModel):

    def __init__(self, raw_data):
        super(Planet, self).__init__(raw_data)

    def __repr__(self):
        return '<Planet - {0}>'.format(self.name)


def _get(id, type):
    result = query("{0}/{1}/{2}/".format(
        BASE_URL,
        type,
        str(id))
    )
    return result


def _search(search_param, type):
    name = quote_plus(search_param)
    result = query("{0}/{1}/?search={2}".format(
        BASE_URL,
        type,
        name)
    )
    return result


def get_planet(planet_id):
    ''' Return a single planet '''
    result = _get(planet_id, PLANETS)
    return Planet(result.content)


def get_planet_appearances(planet_name):
    result = _search(planet_name, PLANETS)
    result = json.loads(result.content)
    if result['count'] == 0:
        return 0
    else:
        times = len(result['results'][0]['films'])
        return times
