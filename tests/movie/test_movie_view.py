import pytest
from django.test import Client
from urllib.request import Request

from tests.factory import StatusFactory

class MonkeyRequest(Request):
    def __init__(self, *args, **kwargs):
        return super().__init__(url='file:./tests/getthumbinfo.xml')

def patch_getthumbinfo(func):
    def wrapper(self, monkeypatch, *args, **kwargs):
        monkeypatch.setattr('movie.views.Request', MonkeyRequest)
        func(self, *args, **kwargs)
    return wrapper

class TestMovieViewAbstract():
    c = Client()

@pytest.mark.django_db
class TestMovieViewIndex(TestMovieViewAbstract):

    @patch_getthumbinfo
    def test_default(self):
        statuses = StatusFactory.create_batch(4)
        statuses += [ StatusFactory(indexes__analyze=False) ]
        response = self.c.get('/movie/')
        # status must be OK
        assert response.status_code == 200
        # not return non-indexed movie
        assert response.context['page_obj'].paginator.count == 4

    @patch_getthumbinfo
    def test_page(self):
        statuses = StatusFactory.create_batch(5)
        response = self.c.get('/movie/', {'page': 2, 'perpage':3})
        # status must be OK
        assert response.status_code == 200
        # returns offset 3
        assert len( response.context['page_obj'].paginator.page(1) ) == 3

    @patch_getthumbinfo
    def test_sortby_postdate(self):
        statuses = StatusFactory.create_batch(5)
        statuses.sort(key=lambda s: s.postdate)
        response = self.c.get('/movie/', {'sortby': 'postdate'})
        # status must be ok
        assert response.status_code == 200
        # ordered by postdate asc
        assert list(response.context['page_obj']) == statuses

    @patch_getthumbinfo
    def test_sortby_postdate_desc(self):
        statuses = StatusFactory.create_batch(5)
        statuses.sort(key=lambda s: s.postdate, reverse=True)
        response = self.c.get('/movie/', {'sortby': '-postdate'})
        # status must be OK
        assert response.status_code == 200
        # ordered by postdate desc
        assert list(response.context['page_obj']) == statuses

    @patch_getthumbinfo
    def test_sortby_maxview_asc(self):
        statuses = StatusFactory.create_batch(5)
        statuses.sort(key=lambda s: s.chart_set.last().view)
        response = self.c.get('/movie/', {'sortby': 'max_view'})
        # status must be OK
        assert response.status_code == 200
        # ordered by max_view asc
        assert list(response.context['page_obj']) == statuses

    @patch_getthumbinfo
    def test_sortby_maxview_desc(self):
        statuses = StatusFactory.create_batch(5)
        statuses.sort(key=lambda s: s.chart_set.last().view, reverse=True)
        response = self.c.get('/movie/', {'sortby': '-max_view'})
        # status must be OK
        assert response.status_code == 200
        # ordered by max_view desc
        assert list(response.context['page_obj']) == statuses

    @patch_getthumbinfo
    def test_not_analyzed(self):
        statuses = StatusFactory.create_batch(4)
        statuses += [ StatusFactory(indexes__analyze=True) ]
        response = self.c.get('/movie/', {'not_analyzed': 'on'})
        # status must be OK
        assert response.status_code == 200
        # returns all tracked movie even if not analyzed
        assert response.context['page_obj'].paginator.count == 5

    @patch_getthumbinfo
    def test_min_view(self):
        statuses = StatusFactory.create_batch(8)
        statuses += [ StatusFactory(charts__max_view=10) ]
        statuses += [ StatusFactory(charts__max_view=100) ]
        statuses += [ StatusFactory(charts__max_view=200) ]
        count = sum(1 for s in statuses if s.chart_set.last().view >= 100 )
        response = self.c.get('/movie/', {'min_view': 100})
        # status must be OK
        assert response.status_code == 200
        # returns max_view >= 100
        assert response.context['page_obj'].paginator.count == count

    @patch_getthumbinfo
    def test_max_view(self):
        statuses = StatusFactory.create_batch(8)
        statuses += [ StatusFactory(charts__max_view=10) ]
        statuses += [ StatusFactory(charts__max_view=100) ]
        statuses += [ StatusFactory(charts__max_view=200) ]
        count = sum(1 for s in statuses if s.chart_set.last().view <= 100 )
        response = self.c.get('/movie/', {'max_view': 100})
        # status must be OK
        assert response.status_code == 200
        # returns max_view <= 100
        assert response.context['page_obj'].paginator.count == count

    @patch_getthumbinfo
    def test_tags(self):
        statuses = StatusFactory.create_batch(5)
        target_tag = statuses[0].idtag_set.first().tagname
        response = self.c.get('/movie/', {'tags': target_tag})
        count = sum(1 for s in statuses if s.idtag_set.filter(tagname=target_tag).exists() )
        # status must be OK
        assert response.status_code == 200
        # returns max_view <= 100
        assert response.context['page_obj'].paginator.count == 1

@pytest.mark.django_db
class TestMovieViewDetail(TestMovieViewAbstract):
    @patch_getthumbinfo
    def test_movie_id(self):
        status = StatusFactory()
        response = self.c.get('/movie/{}/'.format(status.id))
        # status must be OK
        assert response.status_code == 200
        # not return non-indexed movie
        assert response.context['movie'].id == status.id

    @patch_getthumbinfo
    def test_tags(self):
        status = StatusFactory()
        response = self.c.get('/movie/{}/'.format(status.id))
        # status must be OK
        assert response.status_code == 200
        # not return non-indexed movie
        assert set( response.context['tags'].all() ) == set( status.idtag_set.all() )

    @patch_getthumbinfo
    def test_related(self):
        status = StatusFactory.create_batch(13)[0]
        response = self.c.get('/movie/{}/'.format(status.id))
        # status must be OK
        assert response.status_code == 200
        # not return non-indexed movie
        assert response.context['related'].count() == 12

    def test_404(self):
        response = self.c.get('/movie/sm1/')
        assert response.status_code == 404

    def test_redirect(self):
        response = self.c.get('/movie/detail?movie_id=sm1')
        assert response.status_code == 301
