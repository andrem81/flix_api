from rest_framework import serializers
from movies.models import Movie
from django.db.models import Avg
from genres.serializers import GenreSerializer
from actors.serializers import ActorSerializer


class MovieModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'

    def validate_release_date(self, value):
        if value.year < 1990:
            raise serializers.ValidationError(
                'O filme não pode ter data de lançamento menor que 1990.')
        return value

    def validate_resume(self, value):
        if len(value) > 200:
            raise serializers.ValidationError(
                'O resumo do filme não pode ter mais de 200 caracteres.'
            )
        return value


class MovieListDetailSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True)
    genre = GenreSerializer()
    rate = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'genre', 'actors', 'release_date', 'rate', 'resume']

    def get_rate(self, obj):
        rate = obj.reviews.aggregate(Avg('stars'))['stars__avg']

        if rate:
            return round(rate, 1)

        return None
