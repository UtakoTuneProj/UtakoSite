from datetime import timedelta, datetime
import pytest
import json
from django.test import Client

from tests.helpers import StatusCreationHelper as sch

@pytest.mark.django_db
class TestRangeSearchIndex:
    c = Client()
    now = datetime.now()

    def test_default(self):
        sch().create_testcases(dict(
            mvid='sm1',
            postdate=self.now - timedelta(days=8),
            validity=True,
            max_view=90,
            tags=['にこにこ', '初音ミク'],
            index=(1,0,0,0,0,0,0,0),
        ),dict(
            mvid='sm2',
            postdate=self.now - timedelta(days=7),
            validity=True,
            max_view=90,
            tags=['にこにこ', '初音ミク'],
            index=(1,1,0,0,0,0,0,0),
        ),dict(
            mvid='sm3',
            postdate=self.now - timedelta(days=6),
            validity=True,
            max_view=90,
            tags=['にこにこ', '初音ミク'],
            index=(-1,1,0,0,0,0,0,0),
        ))

        response = self.c.get(
            'http://testserver/api/vocalosphere/range/',
            data={
                'range_start': '[0,0,0,0,0,0,0,0]',
                'range_end': '[1,1,1,1,1,1,1,1]'
            },
        )
        result = json.loads(response.content.decode())
        # no data range query must be error
        assert response.status_code == 200
        assert result['count'] == 2

@pytest.mark.django_db
class TestPointSearchIndex:
    c = Client()
    now = datetime.now()

    def test_default(self):
        sch().create_testcases(dict(
            mvid='sm1',
            postdate=self.now - timedelta(days=8),
            validity=True,
            max_view=90,
            tags=['にこにこ', '初音ミク'],
            index=(1,0,0,0,0,0,0,0),
        ),dict(
            mvid='sm2',
            postdate=self.now - timedelta(days=7),
            validity=True,
            max_view=90,
            tags=['にこにこ', '初音ミク'],
            index=(1,1,1,0,0,0,0,0),
        ),dict(
            mvid='sm3',
            postdate=self.now - timedelta(days=6),
            validity=True,
            max_view=90,
            tags=['にこにこ', '初音ミク'],
            index=(1,1,0,0,0,0,0,0),
        ))

        response = self.c.get(
            'http://testserver/api/vocalosphere/point/',
            data={
                'origin': '[1,1,1,1,1,1,1,1]',
            },
        )
        result = json.loads(response.content.decode())
        # no data range query must be error
        assert response.status_code == 200
        assert result['count'] == 3
        assert result['results'][0]['id'] == 'sm2'
        assert result['results'][1]['id'] == 'sm3'
        assert result['results'][2]['id'] == 'sm1'
