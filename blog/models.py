from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    title= models.CharField(max_length= 100)
    content= models.TextField()
    date_posted= models.DateTimeField(default=timezone.now)
    author= models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__ (self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
class Rating(models.Model):
    ONE_TO_FIVE_RATING_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)
    recipe = models.IntegerField()
    rating = models.IntegerField(choices=ONE_TO_FIVE_RATING_CHOICES)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
