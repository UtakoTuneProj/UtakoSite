from datetime import timedelta, datetime
import random
import math
from movie.models import Status, Chart, Idtag, SongIndex, SongRelation, StatusSongRelation

class StatusCreationHelper:
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

