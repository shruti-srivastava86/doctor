from rest_framework.pagination import PageNumberPagination

from api.generics.generics import CustomListAPIView
from doctor.badges.models import Badges
from doctor.badges.serializers import BadgesSerializer


class CustomPaginationClass(PageNumberPagination):
    """
        Custom pagination class
    """
    page_size = 20


class BadgesListView(CustomListAPIView):
    """
        View for listing all badges
    """
    serializer_class = BadgesSerializer
    queryset = Badges.objects.all()
    pagination_class = CustomPaginationClass
