from rest_framework import serializers
from movie_app.models import Director, Movie, Review

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'id name'.split()



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text movie stars movie'.split()


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