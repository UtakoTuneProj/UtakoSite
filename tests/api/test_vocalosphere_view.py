from datetime import timedelta, datetime
import pytest
import json
from django.test import Client

from tests.factory import StatusFactory
from django.db import connection

@pytest.mark.django_db
class TestRangeSearchIndex:
    c = Client()
    now = datetime.now()

    def test_default(self):
        statuses = StatusFactory.create_batch(10)
        count = 0
        count = sum(
            1 for s in statuses\
            if s.songindex_set.last().value0 >= 0
        )
        response = self.c.get(
            'http://testserver/api/vocalosphere/range/',
            data={
                'range_start': '[0,-1,-1,-1,-1,-1,-1,-1]',
                'range_end': '[1,1,1,1,1,1,1,1]'
            },
        )
        result = json.loads(response.content.decode())
        # no data range query must be error
        assert response.status_code == 200
        assert result['count'] == count

@pytest.mark.django_db
class TestPointSearchIndex:
    c = Client()
    now = datetime.now()

    def test_default(self):
        with connection.cursor() as cursor:
            cursor.execute('select load_extension("./libsqlitefunctions");')
        statuses = StatusFactory.create_batch(10)
        origin = statuses[0].songindex_set.last().values
        statuses.sort(
            key = lambda s:\
            sum(
                map(
                    lambda x: (x[0]-x[1])**2, zip(
                    origin,
                    s.songindex_set.last().values
        ))))
        response = self.c.get(
            'http://testserver/api/vocalosphere/point/',
            data={
                'origin': '[{}]'.format(','.join(map(lambda x:'{}'.format(x), origin))),
                'time_factor': 0,
            },
        )
        result = json.loads(response.content.decode())
        #query must be ok
        assert response.status_code == 200
        assert [ x['id'] for x in result['results'] ] == [ s.id for s in statuses ]
