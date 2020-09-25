import factory


class DaysRangeAbstractModelFactory(factory.django.DjangoModelFactory):
    start_range = 1
    end_range = 1
    required_completions = 1
    stage = 1
    challenge = "This is a test challenge"
