from django.db import models

from restaurants.models import Restaurant
from config.models import BaseModel
from users.models import User


class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    comment = models.TextField()

    def __str__(self):
        return f'{self.user} - {self.restaurant}'