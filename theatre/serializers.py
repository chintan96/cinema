import datetime

from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from theatre.models import Movie, Show, Screen, BookedSeat, Seat


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = "__all__"


class ShowSerializer(serializers.ModelSerializer):
    movie = serializers.SlugRelatedField(queryset=Movie.objects.all(), slug_field='id')
    screen = serializers.SlugRelatedField(queryset=Screen.objects.all(), slug_field='number')
    show_time = serializers.DateTimeField(input_formats=["%d-%m-%Y %H:%M:%S"], format="%d-%m-%Y %H:%M:%S")
    end_time = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)
    movie_name = serializers.SerializerMethodField()

    def get_movie_name(self, instance):
        return instance.movie.name

    def create(self, validated_data):
        show_time = validated_data.get("show_time")
        screen = validated_data.get("screen")
        date = show_time.date()
        shows = screen.show_set.filter(show_time__date=date)
        if timezone.now() > show_time:
            raise serializers.ValidationError("Shows cannot be created retroactively.")
        for show in shows:
            if show_time < show.end_time:
                raise serializers.ValidationError("Two shows cannot happen at the same time.")
        show = Show.objects.create(**validated_data)
        for seat in show.screen.seat_set.all():
            BookedSeat.objects.create(seat=seat, show=show)
        return show

    class Meta:
        model = Show
        fields = ["movie", 'screen', "show_time", "end_time", 'id', 'movie_name']
        read_only_fields = ['id']


class SeatSerializer(serializers.ModelSerializer):
    email = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='email', source='user')
    is_available = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        # user = self.context.get("request").user
        # validated_data['user'] = user
        show = validated_data.get('show')
        seat = validated_data.get('seat')
        if timezone.now() > show.show_time:
            raise serializers.ValidationError("Seat cannot be booked after the show starts.")
        try:
            booked_seat = BookedSeat.objects.get(show=show, seat=seat, user__isnull=True)
            with transaction.atomic():
                booked_seat.user = validated_data.get('user')
                booked_seat.save()
        except:
            raise serializers.ValidationError("This seat has already been booked.")
        return booked_seat

    class Meta:
        model = BookedSeat
        fields = ['show', 'seat', 'email', 'is_available']


# class SeatShowSerializer(serializers.ModelSerializer):
