from rest_framework.viewsets import ModelViewSet
from restaurants.serializers import RestaurantSerializer
from restaurants.models import Restaurant


class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer