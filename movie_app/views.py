from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from movie_app.models import Director, Movie, Review
from movie_app.serializers import DirectorSerializer, MovieSerializer, ReviewSerializer

@api_view(['GET', 'POST'])
def director_list_api_view(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        data = DirectorSerializer(directors, many=True).data
        return Response(data={'list': data})
    elif request.method == 'POST':
        print(request.data)
        name = request.data.get('name')
        director = Director.objects.create(
            name= name
        )
        return Response(data= DirectorSerializer(director).data,
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def director_detail_api_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response({'error': 'Режиссер не найден'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = DirectorSerializer(director).data
        return Response(data=data)
    elif request.method == 'PUT':
        director.name = request.data.get('name')
        director.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
def movie_list_api_view(request):
    if request.method == 'GET':
        movie = (Movie.objects.
              prefetch_related('review').all())
        data = MovieSerializer(movie, many=True).data
        return Response(data={'list': data})
    elif request.method == 'POST':
        print(request.data)
        title = request.data.get('title')
        description = request.data.get('description')
        duration = request.data.get('duration')
        director_id = request.data.get('director_id')

        movie = Movie.objects.create(
            title= title,
            description = description,
            duration = duration,
            director_id = director_id
        )
        return Response(data=MovieSerializer(movie).data,
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response({'error': 'Фильм не найден'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = MovieSerializer(movie).data
        return Response(data=data)
    elif request.method == 'PUT':
        movie.title = request.data.get('title')
        movie.description = request.data.get('description')
        movie.duration = request.data.get('duration')
        movie.director_id = request.data.get('director_id')
        movie.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewSerializer(reviews, many=True).data
        return Response(data={'list': data})
    elif request.method == 'POST':
        print(request.data)
        stars = request.data.get('stars')
        text = request.data.get('text')
        movie_id = request.data.get('movie_id')

        review = Review.objects.create(
            stars= stars,
            text= text,
            movie_id= movie_id
        )
        return Response(data=ReviewSerializer(review).data,
                        status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response({'error': 'Отзыв не найден'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewSerializer(review).data
        return Response(data=data)
    elif request.method == 'PUT':
        review.stars =  request.data.get('stars')
        review.text = request.data.get('text')
        review.movie_id = request.data.get('movie_id')
        review.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)