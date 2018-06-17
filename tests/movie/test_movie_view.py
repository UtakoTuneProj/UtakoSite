from datetime import timedelta, datetime
import random
import pytest
import math
from django.test import Client

from movie.models import Status, Chart, Idtag, SongIndex, SongRelation, StatusSongRelation

@pytest.mark.django_db
class TestMovieViewIndex():
    c = Client()
    now = datetime.now()

    def create_testcases(self, *testcases):
        for testcase in testcases:
            self.create_testcase(**testcase)

    def create_testcase(
        self,
        mvid,
        postdate,
        validity,
        max_view,
        tags = None,
        index = None,
    ):
        status = self.create_testcase_status(mvid, postdate, validity)
        self.create_testcase_chart(status, max_view)
        if tags is not None:
            self.create_testcase_idtag(status, tags)
        if index is not None:
            self.create_testcase_songindex(status, index)
            for other_song in Status.objects.all():
                if other_song != status:
                    self.create_testcase_songrelation(status, other_song)

    def create_testcase_status(
        self,
        mvid,
        postdate,
        validity,
    ):
        passed_time = self.now - postdate
        if passed_time < timedelta(days=1, hours=1):
            epoch = passed_time // timedelta(hours=1) + 1
        elif passed_time < timedelta(days=7, hours=1):
            epoch = 24
        else:
            epoch = 25
        iscomplete = True if epoch == 25 and validity else False

        return Status.objects.create(
            id = mvid,
            validity = validity,
            iscomplete = iscomplete,
            epoch = epoch,
            postdate = postdate,
            analyzegroup = random.randrange(19) if iscomplete else None,
        )

    def create_testcase_chart(
        self,
        status,
        max_view
    ):
        v = 0
        c = 0
        m = 0
        for i in range(status.epoch):
            if i == status.epoch - 1:
                v = max_view
                c = max_view // 10
                m = max_view // 10
            else:
                v = min(random.randrange(v, v+100), max_view)
                c = min(random.randrange(c, c+10) , max_view // 10)
                m = min(random.randrange(m, m+10) , max_view // 10)
            Chart.objects.create(
                status = status,
                epoch = i,
                time = (2*i + 1) * 30 if i != 24 else 10140,
                view = v,
                comment = c,
                mylist = m,
            )

    def create_testcase_idtag(
        self,
        status,
        tags,
    ):
        for tag in tags:
            Idtag.objects.create(
                status=status,
                tagname=tag,
                count=1,
            )

    def create_testcase_songindex(
        self,
        status,
        index,
    ):
        dic = dict(status=status,version=0)
        for i in range(8):
            dic['value{}'.format(i)] = index[i]
        SongIndex.objects.create(
            **dic
        )

    def create_testcase_songrelation(
        self,
        origin,
        dest,
    ):
        def distance(origin, dest):
            R2 = 0
            for i in range(8):
                origin_axis = getattr(origin.songindex_set.get(version=0), 'value{}'.format(i))
                dest_axis = getattr(dest.songindex_set.get(version=0), 'value{}'.format(i))
                R2 += (origin_axis - dest_axis)**2
            return math.sqrt(R2)

        rel = SongRelation.objects.create(
            distance=distance(origin, dest),
            version=0,
        )
        StatusSongRelation.objects.create(
            status=origin,
            song_relation=rel,
        )
        StatusSongRelation.objects.create(
            status=dest,
            song_relation=rel,
        )

    def test_default(self):
        self.create_testcases(dict(
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
        assert response.context['movies'].paginator.count == 2
    
    def test_page(self):
        self.create_testcases(dict(
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
        assert len(response.context['movies'].object_list) == 1
    
    def test_sortby_postdate(self):
        self.create_testcases(dict(
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
        assert list(map(lambda x: getattr(x, 'id'), response.context['movies'].object_list )) == ['sm1', 'sm2', 'sm3', 'sm4']

    def test_sortby_postdate_desc(self):
        self.create_testcases(dict(
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
        assert list(map(lambda x: getattr(x, 'id'), response.context['movies'].object_list )) == ['sm4', 'sm3', 'sm2', 'sm1']
    
    def test_sortby_maxview_asc(self):
        self.create_testcases(dict(
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
        assert list(map(lambda x: getattr(x, 'id'), response.context['movies'].object_list )) == ['sm3', 'sm4', 'sm1', 'sm2']
    
    def test_sortby_maxview_desc(self):
        self.create_testcases(dict(
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
        assert list(map(lambda x: getattr(x, 'id'), response.context['movies'].object_list )) == ['sm2', 'sm1', 'sm4', 'sm3']
    
    def test_not_isanalyzed(self):
        self.create_testcases(dict(
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
        response = self.c.get('/movie/', {'isanalyzed': 'off'})
        # status must be OK
        assert response.status_code == 200
        # returns all tracked movie even if not analyzed
        assert response.context['movies'].paginator.count == 4
    
    def test_min_view(self):
        self.create_testcases(dict(
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
        assert response.context['movies'].paginator.count == 3
    
    def test_max_view(self):
        self.create_testcases(dict(
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
        assert response.context['movies'].paginator.count == 3

    def test_tags(self):
        self.create_testcases(dict(
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
        assert response.context['movies'].paginator.count == 3
