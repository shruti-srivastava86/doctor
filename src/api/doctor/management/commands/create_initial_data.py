from django.core.management.base import BaseCommand
from django.db import transaction

from doctor.badges.models import Badges
from doctor.food_hydration.models import (
    FoodAndHydrationDaysRange
)
from doctor.management.commands.surrounding_initial_data import (
    surrounding_initial_data
)
from doctor.management.commands.badges_initial_data import (
    badges_initial_data
)
from doctor.management.commands.food_and_hydration_initial_data import (
    food_and_hydration_initial_data
)
from doctor.management.commands.mind_initial_data import (
    mind_initial_data
)
from doctor.management.commands.motion_initial_data import (
    motion_initial_data
)
from doctor.management.commands.sleep_initial_data import (
    sleep_initial_data
)
from doctor.management.commands.weight_initial_data import (
    weight_initial_data
)
from doctor.mind.models import MindDaysRange
from doctor.motion.models import MotionDaysRange
from doctor.sleep.models import SleepDaysRange
from doctor.surrounding.models import SurroundingDaysRange
from doctor.weight.models import WeightDaysRange


class Command(BaseCommand):
    help = 'Create days range for each assessments'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                if not WeightDaysRange.objects.first_day_range().first():
                    WeightDaysRange.objects.bulk_create(
                        [
                            WeightDaysRange(**data) for data in weight_initial_data
                        ]
                    )
                if not FoodAndHydrationDaysRange.objects.first_day_range().first():
                    FoodAndHydrationDaysRange.objects.bulk_create(
                        [
                            FoodAndHydrationDaysRange(**data) for data in food_and_hydration_initial_data
                        ]
                    )
                if not MotionDaysRange.objects.first_day_range().first():
                    MotionDaysRange.objects.bulk_create(
                        [
                            MotionDaysRange(**data) for data in motion_initial_data
                        ]
                    )
                if not SleepDaysRange.objects.first_day_range().first():
                    SleepDaysRange.objects.bulk_create(
                        [
                            SleepDaysRange(**data) for data in sleep_initial_data
                        ]
                    )
                if not MindDaysRange.objects.first_day_range().first():
                    MindDaysRange.objects.bulk_create(
                        [
                            MindDaysRange(**data) for data in mind_initial_data
                        ]
                    )
                if not Badges.objects.all():
                    Badges.objects.bulk_create(
                        [
                            Badges(**data) for data in badges_initial_data
                        ]
                    )
                if not SurroundingDaysRange.objects.all():
                    SurroundingDaysRange.objects.bulk_create(
                        [
                            SurroundingDaysRange(**data) for data in surrounding_initial_data
                        ]
                    )
            self.stdout.write(self.style.SUCCESS('Successfully created initial data'))
        except Exception as error:
            self.stdout.write(self.style.ERROR('Failed to create initial data. Error: {}'.format(str(error))))
