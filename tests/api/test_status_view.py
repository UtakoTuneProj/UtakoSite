from datetime import timedelta, datetime
import pytest
import json
from django.test import Client

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
        ))
        response = self.c.get('/api/movie/')
        result = json.loads(response.content.decode())
        # status must be OK
        assert response.status_code == 200
        # not return non-indexed movie
        assert result['count'] == 2

    def test_sortby_postdate(self):
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
            index=(1,0,1,0,0,0,0,0),
        ),dict(
            mvid='sm4',
            postdate=self.now - timedelta(days=5),
            validity=True,
            max_view=90,
            tags=['にこにこ', '初音ミク'],
            index=(1,0,0,1,0,0,0,0),
        ))
        response = self.c.get('/api/movie/', {'sortby': 'postdate'})
        result = json.loads(response.content.decode())
        # status must be ok
        assert response.status_code == 200
        # ordered by postdate asc
        assert list(map(lambda x: x['id'], result['results'] )) == ['sm1', 'sm2', 'sm3', 'sm4']

    def test_sortby_postdate_desc(self):
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
            index=(1,0,1,0,0,0,0,0),
        ),dict(
            mvid='sm4',
            postdate=self.now - timedelta(days=5),
            validity=True,
            max_view=90,
            tags=['にこにこ', '初音ミク'],
            index=(1,0,0,1,0,0,0,0),
        ))
        response = self.c.get('/api/movie/', {'sortby': '-postdate'})
        result = json.loads(response.content.decode())
        # status must be OK
        assert response.status_code == 200
        # ordered by postdate desc
        assert list(map(lambda x: x['id'], result['results'] )) == ['sm4', 'sm3', 'sm2', 'sm1']

    def test_sortby_maxview_asc(self):
        sch().create_testcases(dict(
            mvid='sm1',
            postdate=self.now - timedelta(days=8),
            validity=True,
            max_view=900,
            tags=['にこにこ', '初音ミク'],
            index=(1,0,0,0,0,0,0,0),
        ),dict(
            mvid='sm2',
            postdate=self.now - timedelta(days=7),
            validity=True,
            max_view=9000,
            tags=['にこにこ', '初音ミク'],
            index=(1,1,0,0,0,0,0,0),
        ),dict(
            mvid='sm3',
            postdate=self.now - timedelta(days=6),
            validity=True,
            max_view=9,
            tags=['にこにこ', '初音ミク'],
            index=(1,0,1,0,0,0,0,0),
        ),dict(
            mvid='sm4',
            postdate=self.now - timedelta(days=5),
            validity=True,
            max_view=90,
            tags=['にこにこ', '初音ミク'],
            index=(1,0,0,1,0,0,0,0),
        ))
        response = self.c.get('/api/movie/', {'sortby': 'max_view'})
        result = json.loads(response.content.decode())
        # status must be OK
        assert response.status_code == 200
        # ordered by max_view asc
        assert list(map(lambda x: x['id'], result['results']  )) == ['sm3', 'sm4', 'sm1', 'sm2']

    def test_sortby_maxview_desc(self):
        sch().create_testcases(dict(
            mvid='sm1',
            postdate=self.now - timedelta(days=8),
            validity=True,
            max_view=900,
            tags=['にこにこ', '初音ミク'],
            index=(1,0,0,0,0,0,0,0),
        ),dict(
            mvid='sm2',
            postdate=self.now - timedelta(days=7),
            validity=True,
            max_view=9000,
            tags=['にこにこ', '初音ミク'],
            index=(1,1,0,0,0,0,0,0),
        ),dict(
            mvid='sm3',
            postdate=self.now - timedelta(days=6),
            validity=True,
            max_view=9,
            tags=['にこにこ', '初音ミク'],
            index=(1,0,1,0,0,0,0,0),
        ),dict(
            mvid='sm4',
            postdate=self.now - timedelta(days=5),
            validity=True,
            max_view=90,
            tags=['にこにこ', '初音ミク'],
            index=(1,0,0,1,0,0,0,0),
        ))
        response = self.c.get('/api/movie/', {'sortby': '-max_view'})
        result = json.loads(response.content.decode())
        # status must be OK
        assert response.status_code == 200
        # ordered by max_view desc
        assert list(map(lambda x: x['id'], result['results'] )) == ['sm2', 'sm1', 'sm4', 'sm3']

    def test_not_analyzed(self):
        sch().create_testcases(dict(
            mvid='sm1',
            postdate=self.now - timedelta(days=8),
            validity=True,
            max_view=900,
            tags=['にこにこ', '初音ミク'],
            index=(1,0,0,0,0,0,0,0),
        ),dict(
            mvid='sm2',
            postdate=self.now - timedelta(days=7),
            validity=True,
            max_view=9000,
            tags=['にこにこ', '初音ミク'],
            index=(1,1,0,0,0,0,0,0),
        ),dict(
            mvid='sm3',
            postdate=self.now - timedelta(days=6),
            validity=True,
            max_view=9,
            tags=['にこにこ', '初音ミク'],
        ),dict(
            mvid='sm4',
            postdate=self.now - timedelta(days=5),
            validity=True,
            max_view=90,
            tags=['にこにこ', '初音ミク'],
        ))
        response = self.c.get('/api/movie/', {'not_analyzed': 'on'})
        result = json.loads(response.content.decode())
        # status must be OK
        assert response.status_code == 200
        # returns all tracked movie even if not analyzed
        assert result['count'] == 4

    def test_min_view(self):
        sch().create_testcases(dict(
            mvid='sm1',
            postdate=self.now - timedelta(days=8),
            validity=True,
            max_view=900,
            tags=['にこにこ', '初音ミク'],
            index=(1,0,0,0,0,0,0,0),
        ),dict(
            mvid='sm2',
            postdate=self.now - timedelta(days=7),
            validity=True,
            max_view=9000,
            tags=['にこにこ', '初音ミク'],
            index=(1,1,0,0,0,0,0,0),
        ),dict(
            mvid='sm3',
            postdate=self.now - timedelta(days=6),
            validity=True,
            max_view=9,
            tags=['にこにこ', '初音ミク'],
            index=(1,0,1,0,0,0,0,0),
        ),dict(
            mvid='sm4',
            postdate=self.now - timedelta(days=5),
            validity=True,
            max_view=100,
            tags=['にこにこ', '初音ミク'],
            index=(1,0,1,0,0,0,0,0),
        ))
        response = self.c.get('/api/movie/', {'min_view': 100})
        result = json.loads(response.content.decode())
        # status must be OK
        assert response.status_code == 200
        # returns max_view >= 100
        assert result['count'] == 3

    def test_max_view(self):
        sch().create_testcases(dict(
            mvid='sm1',
            postdate=self.now - timedelta(days=8),
            validity=True,
            max_view=100,
            tags=['にこにこ', '初音ミク'],
            index=(1,0,0,0,0,0,0,0),
        ),dict(
            mvid='sm2',
            postdate=self.now - timedelta(days=7),
            validity=True,
            max_view=9000,
            tags=['にこにこ', '初音ミク'],
            index=(1,1,0,0,0,0,0,0),
        ),dict(
            mvid='sm3',
            postdate=self.now - timedelta(days=6),
            validity=True,
            max_view=9,
            tags=['にこにこ', '初音ミク'],
            index=(1,0,1,0,0,0,0,0),
        ),dict(
            mvid='sm4',
            postdate=self.now - timedelta(days=5),
            validity=True,
            max_view=90,
            tags=['にこにこ', '初音ミク'],
            index=(1,0,1,0,0,0,0,0),
        ))
        response = self.c.get('/api/movie/', {'max_view': 100})
        result = json.loads(response.content.decode())
        # status must be OK
        assert response.status_code == 200
        # returns max_view <= 100
        assert result['count'] == 3

    def test_tags(self):
        sch().create_testcases(dict(
            mvid='sm1',
            postdate=self.now - timedelta(days=8),
            validity=True,
            max_view=100,
            tags=['にこにこ', '初音ミク'],
            index=(1,0,0,0,0,0,0,0),
        ),dict(
            mvid='sm2',
            postdate=self.now - timedelta(days=7),
            validity=True,
            max_view=9000,
            tags=['にこにこ', '初音ミク'],
            index=(1,1,0,0,0,0,0,0),
        ),dict(
            mvid='sm3',
            postdate=self.now - timedelta(days=6),
            validity=True,
            max_view=9,
            tags=['にこにこ', '初音ミク'],
            index=(1,0,1,0,0,0,0,0),
        ),dict(
            mvid='sm4',
            postdate=self.now - timedelta(days=5),
            validity=True,
            max_view=90,
            tags=['にこにこ', 'GUMI'],
            index=(1,0,1,0,0,0,0,0),
        ))
        response = self.c.get('/api/movie/', {'tags': '初音ミク'})
        result = json.loads(response.content.decode())
        # status must be OK
        assert response.status_code == 200
        # returns max_view <= 100
        assert result['count'] == 3

@pytest.mark.django_db
class TestMovieViewDetail:
    c = Client()
    now = datetime.now()

    def test_movie_id(self):
        sch().create_testcases(dict(
            mvid='sm1',
            postdate=self.now - timedelta(days=8),
            validity=True,
            max_view=90,
            tags=['にこにこ', '初音ミク'],
            index=(1,0,0,0,0,0,0,0),
        ))
        response = self.c.get('/api/movie/sm1/')
        result = json.loads(response.content.decode())
        # status must be OK
        assert response.status_code == 200
        # not return non-indexed movie
        assert result['id'] == 'sm1'

    def test_404(self):
        response = self.c.get('/api/movie/sm1/')
        assert response.status_code == 404
