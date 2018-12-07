from datetime import timedelta, datetime
import pytest
import json
from django.test import Client

from tests.factory import StatusFactory

@pytest.mark.django_db
class TestMovieViewIndex:
    c = Client()
    now = datetime.now()

    def test_default(self):
        statuses = StatusFactory.create_batch(4)
        statuses += [ StatusFactory(indexes__analyze=False) ]
        response = self.c.get('/api/movie/')
        result = json.loads(response.content.decode())
        # status must be OK
        assert response.status_code == 200
        # not return non-indexed movie
        assert result['count'] == 4

    def test_sortby_postdate(self):
        statuses = StatusFactory.create_batch(5)
        statuses.sort(key=lambda s: s.postdate)
        response = self.c.get('/api/movie/', {'sortby': 'postdate'})
        result = json.loads(response.content.decode())
        # status must be ok
        assert response.status_code == 200
        # ordered by postdate asc
        assert list(map(lambda x: x['id'], result['results'] )) == [x.id for x in statuses]

    def test_sortby_postdate_desc(self):
        statuses = StatusFactory.create_batch(5)
        statuses.sort(key=lambda s: s.postdate, reverse=True)
        response = self.c.get('/api/movie/', {'sortby': '-postdate'})
        result = json.loads(response.content.decode())
        # status must be OK
        assert response.status_code == 200
        # ordered by postdate desc
        assert list(map(lambda x: x['id'], result['results'] )) == [x.id for x in statuses]

    def test_sortby_maxview_asc(self):
        statuses = StatusFactory.create_batch(5)
        statuses.sort(key=lambda s: s.chart_set.last().view)
        response = self.c.get('/api/movie/', {'sortby': 'max_view'})
        result = json.loads(response.content.decode())
        # status must be OK
        assert response.status_code == 200
        # ordered by max_view asc
        assert list(map(lambda x: x['id'], result['results'] )) == [x.id for x in statuses]

    def test_sortby_maxview_desc(self):
        statuses = StatusFactory.create_batch(5)
        statuses.sort(key=lambda s: s.chart_set.last().view, reverse=True)
        response = self.c.get('/api/movie/', {'sortby': '-max_view'})
        result = json.loads(response.content.decode())
        # status must be OK
        assert response.status_code == 200
        # ordered by max_view desc
        assert list(map(lambda x: x['id'], result['results'] )) == [x.id for x in statuses]

    def test_not_analyzed(self):
        statuses = StatusFactory.create_batch(4)
        statuses += [ StatusFactory(indexes__analyze=False) ]
        response = self.c.get('/api/movie/', {'not_analyzed': 'on'})
        result = json.loads(response.content.decode())
        # status must be OK
        assert response.status_code == 200
        # returns all tracked movie even if not analyzed
        assert result['count'] == 5

    def test_min_view(self):
        statuses = StatusFactory.create_batch(8)
        statuses += [ StatusFactory(charts__max_view=10) ]
        statuses += [ StatusFactory(charts__max_view=100) ]
        statuses += [ StatusFactory(charts__max_view=200) ]
        count = sum(1 for s in statuses if s.chart_set.last().view >= 100 )
        response = self.c.get('/api/movie/', {'min_view': 100})
        result = json.loads(response.content.decode())
        # status must be OK
        assert response.status_code == 200
        # returns max_view >= 100
        assert result['count'] == count

    def test_max_view(self):
        statuses = StatusFactory.create_batch(8)
        statuses += [ StatusFactory(charts__max_view=10) ]
        statuses += [ StatusFactory(charts__max_view=100) ]
        statuses += [ StatusFactory(charts__max_view=200) ]
        count = sum(1 for s in statuses if s.chart_set.last().view <= 100 )
        response = self.c.get('/api/movie/', {'max_view': 100})
        result = json.loads(response.content.decode())
        # status must be OK
        assert response.status_code == 200
        # returns max_view <= 100
        assert result['count'] == count

    def test_tags(self):
        statuses = StatusFactory.create_batch(5)
        target_tag = statuses[0].idtag_set.first().tagname
        count = sum(1 for s in statuses if s.idtag_set.filter(tagname=target_tag).exists() )
        response = self.c.get('/api/movie/', {'tags': target_tag})
        result = json.loads(response.content.decode())
        # status must be OK
        assert response.status_code == 200
        # returns max_view <= 100
        assert result['count'] == count

@pytest.mark.django_db
class TestMovieViewDetail:
    c = Client()
    now = datetime.now()

    def test_movie_id(self):
        status = StatusFactory()
        response = self.c.get('/api/movie/{}/'.format(status.id))
        result = json.loads(response.content.decode())
        # status must be OK
        assert response.status_code == 200
        # not return non-indexed movie
        assert result['id'] == status.id

    def test_404(self):
        response = self.c.get('/api/movie/sm1/')
        assert response.status_code == 404
