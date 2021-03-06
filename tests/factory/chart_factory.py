import factory
import faker
from movie.models import Chart

fake = faker.Faker()

class ChartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Chart

    class Params:
        max_view = factory.LazyFunction( lambda: fake.random.randint(10, 5000) )

    status = factory.SubFactory('tests.factory.StatusFactory')

    @factory.lazy_attribute
    def epoch(self):
        if self.status.chart_set.exists():
            return self.status.chart_set.last().epoch + 1
        else:
            return 0

    @factory.lazy_attribute
    def view(self):
        if self.status.chart_set.exists():
            return fake.random.randint(
                a=self.status.chart_set.last().view,
                b=self.max_view
            ) if self.epoch != 24 else self.max_view
        else:
            return fake.random.randrange(self.max_view)

    @factory.lazy_attribute
    def comment(self):
        if self.status.chart_set.exists():
            return fake.random.randint(
                a=self.status.chart_set.last().comment,
                b=self.max_view // 10
            ) if self.epoch != 24 else self.max_view // 10
        else:
            return fake.random.randrange(self.max_view // 10)

    @factory.lazy_attribute
    def mylist(self):
        if self.status.chart_set.exists():
            return fake.random.randint(
                a=self.status.chart_set.last().mylist,
                b=self.max_view // 10
            ) if self.epoch != 24 else self.max_view // 10
        else:
            return fake.random.randrange(self.max_view // 10)

    @factory.lazy_attribute
    def time(self):
        i = self.epoch
        return (2*i + 1) * 30 if i != 24 else 10140
