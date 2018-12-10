import factory
from movie.models import SongIndex, Status, StatusSongRelation, SongRelation
import math
from random import random

randomindex = lambda: random() * 2 - 1

class SongIndexFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SongIndex

    status = factory.SubFactory('tests.factory.StatusFactory')
    value0 = factory.LazyFunction(randomindex)
    value1 = factory.LazyFunction(randomindex)
    value2 = factory.LazyFunction(randomindex)
    value3 = factory.LazyFunction(randomindex)
    value4 = factory.LazyFunction(randomindex)
    value5 = factory.LazyFunction(randomindex)
    value6 = factory.LazyFunction(randomindex)
    value7 = factory.LazyFunction(randomindex)
    version = 0

    @factory.post_generation
    def create_relations(obj, create, extracted, **kwargs):
        def create_relation(origin, dest):
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

        for target in Status.objects.all():
            if target != obj.status:
                create_relation(obj.status, target)
