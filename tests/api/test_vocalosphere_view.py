from datetime import timedelta, datetime
import pytest
import json
from rest_framework.test import RequestsClient as Client

from tests.helpers import StatusCreationHelper as sch

@pytest.mark.django_db
class TestMovieViewIndex:
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
        response = self.c.post(
                'http://testserver/api/vocalosphere/range/',
            {
                'range_start': [0,0,0,0,0,0,0,0],
                'range_end': [1,1,1,1,1,1,1,1]
            },
        )
        result = json.loads(response.content.decode())
        # no data range query must be error
        assert response.status_code == 200
        assert result['count'] == 2
