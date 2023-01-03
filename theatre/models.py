import datetime

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.


class Movie(models.Model):
    name = models.CharField(max_length=64)
    genre = models.CharField(max_length=64)
    director = models.CharField(max_length=64)
    runtime = models.DurationField(default=datetime.timedelta(0))

    class Meta:
        constraints = [models.UniqueConstraint(fields=['name', 'director'], name="director_movie")]


class Screen(models.Model):
    number = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])


class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    show_time = models.DateTimeField(default=datetime.datetime.now)

    @property
    def end_time(self):
        return self.show_time + self.movie.runtime


class Seat(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    row_number = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    column_number = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])

    class Meta:
        constraints = [models.UniqueConstraint(fields=['screen', 'row_number', 'column_number'], name="individual_seat")]


class BookedSeat(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    @property
    def is_available(self):
        flag = True if not self.user else False
        return flag

    class Meta:
        constraints = [models.UniqueConstraint(fields=['seat', 'show'], name='show_seat')]
