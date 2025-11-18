from django.db.models import Count, Avg
from rest_framework import generics, views, response, status
from rest_framework.permissions import IsAuthenticated
from movies.models import Movie
from movies.serializers import MovieModelSerializer, MovieListDetailSerializer
from app.permissions import GlobalDefaultPermission
from reviews.models import Review


class MovieCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MovieListDetailSerializer
        return MovieModelSerializer


class MovieRetriveUpdatetDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MovieListDetailSerializer
        return MovieModelSerializer


class MoviesStatsView(views.APIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Movie.objects.all()

    def get(self, request):
        total_movies = self.queryset.count()
        movies_by_genres = self.queryset.values('genre__name').annotate(
            count=Count('id'))
        total_reviews = Review.objects.count()
        avarage_stars = Review.objects.aggregate(
            avg_stars=Avg('stars'))['avg_stars']

        return response.Response(data={
            'total_movies': total_movies,
            'movies_by_genres': movies_by_genres,
            'total_reviews': total_reviews,
            'avarage_stars': round(avarage_stars, 1)
            if avarage_stars else 0,
        }, status=status.HTTP_200_OK,
        )
