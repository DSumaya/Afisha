from rest_framework import serializers
from movie_app.models import Director, Movie, Review
from rest_framework.exceptions import ValidationError

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'id name'.split()

# Validation
class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, min_length=2)



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text movie stars movie'.split()

#Vlaidation
class ReviewValidateSerializer(serializers.Serializer):
    stars = serializers.IntegerField(min_value=1, max_value=5)
    text = serializers.CharField()
    movie_id = serializers.IntegerField(min_value=1)

    def validate_movie_id(self, movie_id):
        try:
            Movie.objects.get(id = movie_id)
        except:
            raise ValidationError('Category not exist!')
        return movie_id


class MovieSerializer(serializers.ModelSerializer):
    review = ReviewSerializer(many=True, read_only=True)
    review_name = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = 'id title description duration director review review_name '.split()

    def get_review_name(self, movie):
        if movie.review.all():
            return movie.review.name
        return None

class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, min_length=5)
    description = serializers.CharField()
    duration = serializers.FloatField()
    director_id = serializers.IntegerField(min_value=1)

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id = director_id)
        except:
            raise ValidationError('Category not exist!')
        return director_id

