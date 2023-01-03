from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.decorators import action

from theatre.models import Movie, Show, BookedSeat, Seat
from theatre.serializers import MovieSerializer, ShowSerializer, SeatSerializer


# Create your views here.


class MovieViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()


class ShowViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer


class SeatViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    serializer_class = SeatSerializer

    def get_queryset(self):
        show = self.request.query_params.get("show")
        return BookedSeat.objects.filter(show_id=int(show))
