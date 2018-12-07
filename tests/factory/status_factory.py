import factory
import faker
from movie.models import Status
from datetime import timedelta, datetime
from . import ChartFactory, IdtagFactory, SongIndexFactory

fake = faker.Faker()

class StatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Status

    id = factory.Sequence(lambda x: 'sm{}'.format(x))
    validity = True
    postdate = factory.LazyAttribute(lambda obj: datetime.now() - timedelta(days=8))

    @factory.lazy_attribute
    def epoch(self):
        passed_time = datetime.now() - self.postdate
        if passed_time < timedelta(days=1, hours=1):
            epoch = passed_time // timedelta(hours=1) + 1
        elif passed_time < timedelta(days=7, hours=1):
            epoch = 24
        else:
            epoch = 25
        return epoch

    @factory.lazy_attribute
    def iscomplete(self):
        return True if self.epoch == 25 and self.validity else False

    @factory.post_generation
    def charts(obj, create, extracted, **kwvars):
        kwargs = {'max_view': fake.random.randint(10, 5000)}
        kwargs.update(kwvars)
        ChartFactory.create_batch(obj.epoch, status=obj, **kwargs)

    @factory.post_generation
    def tags(obj, create, extracted, **kwargs):
        for i, tag in enumerate( fake.words(nb=10, unique=True) ):
            if 'tags' in kwargs and len(kwargs['tags']) > i:
                IdtagFactory.create(status=obj, tagname=kwargs['tags'][i])
            else:
                IdtagFactory.create(status=obj, tagname=tag)

    @factory.post_generation
    def indexes(obj, create, extracted, **kwargs):
        if kwargs.get('analyze', True):
            SongIndexFactory(status=obj)
