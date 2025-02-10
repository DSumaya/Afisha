from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from movie_app.models import Director, Movie, Review
from movie_app.serializers import DirectorSerializer, MovieSerializer, ReviewSerializer

@api_view(['GET'])
def director_list_api_view(request):
    directors = Director.objects.all()
    data = DirectorSerializer(directors, many=True).data
    return Response(data={'list': data})

@api_view(['GET'])
def director_detail_api_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response({'error': 'Режиссер не найден'}, status=status.HTTP_404_NOT_FOUND)
    data = DirectorSerializer(director).data
    return Response(data=data)



@api_view(['GET'])
def movie_list_api_view(request):
    movies = (Movie.objects.
              prefetch_related('review').all())
    data = MovieSerializer(movies, many=True).data
    return Response(data={'list': data})

@api_view(['GET'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response({'error': 'Фильм не найден'}, status=status.HTTP_404_NOT_FOUND)
    data = MovieSerializer(movie).data
    return Response(data=data)



@api_view(['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    data = ReviewSerializer(reviews, many=True).data
    return Response(data={'list': data})

@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response({'error': 'Отзыв не найден'}, status=status.HTTP_404_NOT_FOUND)
    data = ReviewSerializer(review).data
    return Response(data=data)


