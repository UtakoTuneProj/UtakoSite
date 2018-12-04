import factory
import faker
from movie.models import Idtag

fake = faker.Faker()

class IdtagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Idtag

    status = factory.SubFactory('tests.factory.StatusFactory')
    tagname = fake.word()
    count = 1
