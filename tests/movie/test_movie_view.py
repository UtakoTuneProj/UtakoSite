import pytest
import math
from datetime import datetime, timedelta
from django.test import Client

from tests.helpers import StatusCreationHelper as sch

@pytest.mark.django_db
class TestMovieViewIndex():
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
        response = self.c.get('/movie/')
        # status must be OK
        assert response.status_code == 200
        # not return non-indexed movie
        assert response.context['page_obj'].paginator.count == 2

    def test_page(self):
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
        response = self.c.get('/movie/', {'page': 2, 'perpage':3})
        # status must be OK
        assert response.status_code == 200
        # returns offset 3
        assert len(response.context['page_obj'].object_list) == 1

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
        response = self.c.get('/movie/', {'sortby': 'postdate'})
        # status must be ok
        assert response.status_code == 200
        # ordered by postdate asc
        assert list(map(lambda x: getattr(x, 'id'), response.context['page_obj'].object_list )) == ['sm1', 'sm2', 'sm3', 'sm4']

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
        response = self.c.get('/movie/', {'sortby': '-postdate'})
        # status must be OK
        assert response.status_code == 200
        # ordered by postdate desc
        assert list(map(lambda x: getattr(x, 'id'), response.context['page_obj'].object_list )) == ['sm4', 'sm3', 'sm2', 'sm1']

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
        response = self.c.get('/movie/', {'sortby': 'max_view'})
        # status must be OK
        assert response.status_code == 200
        # ordered by max_view asc
        assert list(map(lambda x: getattr(x, 'id'), response.context['page_obj'].object_list )) == ['sm3', 'sm4', 'sm1', 'sm2']

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
        response = self.c.get('/movie/', {'sortby': '-max_view'})
        # status must be OK
        assert response.status_code == 200
        # ordered by max_view desc
        assert list(map(lambda x: getattr(x, 'id'), response.context['page_obj'].object_list )) == ['sm2', 'sm1', 'sm4', 'sm3']

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
        response = self.c.get('/movie/', {'not_analyzed': 'on'})
        # status must be OK
        assert response.status_code == 200
        # returns all tracked movie even if not analyzed
        assert response.context['page_obj'].paginator.count == 4

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
        response = self.c.get('/movie/', {'min_view': 100})
        # status must be OK
        assert response.status_code == 200
        # returns max_view >= 100
        assert response.context['page_obj'].paginator.count == 3

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
        response = self.c.get('/movie/', {'max_view': 100})
        # status must be OK
        assert response.status_code == 200
        # returns max_view <= 100
        assert response.context['page_obj'].paginator.count == 3

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
        response = self.c.get('/movie/', {'tags': '初音ミク'})
        # status must be OK
        assert response.status_code == 200
        # returns max_view <= 100
        assert response.context['page_obj'].paginator.count == 3

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
        response = self.c.get('/movie/sm1/')
        # status must be OK
        assert response.status_code == 200
        # not return non-indexed movie
        assert response.context['movie'].id == 'sm1'

    def test_tags(self):
        sch().create_testcases(dict(
            mvid='sm1',
            postdate=self.now - timedelta(days=8),
            validity=True,
            max_view=90,
            tags=['にこにこ', '初音ミク'],
            index=(1,0,0,0,0,0,0,0),
        ))
        response = self.c.get('/movie/sm1/')
        # status must be OK
        assert response.status_code == 200
        # not return non-indexed movie
        assert 'にこにこ' in list(map(lambda x: getattr(x, 'tagname'), response.context['tags'] ))
        assert '初音ミク' in list(map(lambda x: getattr(x, 'tagname'), response.context['tags'] ))

    def test_related(self):
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
            index=(1,1,1,0,0,0,0,0),
        ),dict(
            mvid='sm4',
            postdate=self.now - timedelta(days=5),
            validity=True,
            max_view=90,
            tags=['にこにこ', '初音ミク'],
            index=(1,1,1,0,0,0,0,0),
        ))
        response = self.c.get('/movie/sm1/')
        # status must be OK
        assert response.status_code == 200
        # not return non-indexed movie
        assert list(map(lambda x: getattr(x, 'destination'), response.context['related'] )) == ['sm2', 'sm3', 'sm4']

    def test_404(self):
        response = self.c.get('/movie/sm1/')
        assert response.status_code == 404

    def test_redirect(self):
        response = self.c.get('/movie/detail?movie_id=sm1')
        assert response.status_code == 301
