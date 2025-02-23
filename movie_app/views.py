from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from movie_app.models import Director, Movie, Review
from movie_app.serializers import (DirectorSerializer, MovieSerializer, ReviewSerializer,
                                   DirectorValidateSerializer, ReviewValidateSerializer, MovieValidateSerializer)
from rest_framework.views import APIView

class DirectorListAPIView(APIView):
    def get(self, request):
        directors = Director.objects.all()
        data = DirectorSerializer(directors, many=True).data
        return Response(data={'list': data})

    def post(self, request):
        serializer = DirectorValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        director = Director.objects.create(name=serializer.validated_data.get('name'))
        return Response(data=DirectorSerializer(director).data, status=status.HTTP_201_CREATED)


class DirectorDetailAPIView(APIView):
    def get_object(self, id):
        try:
            return Director.objects.get(id=id)
        except Director.DoesNotExist:
            return None

    def get(self, request, id):
        director = self.get_object(id)
        if not director:
            return Response({'error': 'Режиссер не найден'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data=DirectorSerializer(director).data)

    def put(self, request, id):
        director = self.get_object(id)
        if not director:
            return Response({'error': 'Режиссер не найден'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DirectorValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        director.name = serializer.validated_data.get('name')
        director.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        director = self.get_object(id)
        if not director:
            return Response({'error': 'Режиссер не найден'}, status=status.HTTP_404_NOT_FOUND)
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieListAPIView(APIView):
    def get(self, request):
        movies = Movie.objects.prefetch_related('review').all()
        data = MovieSerializer(movies, many=True).data
        return Response(data={'list': data})

    def post(self, request):
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        movie = Movie.objects.create(**serializer.validated_data)
        return Response(data=MovieSerializer(movie).data, status=status.HTTP_201_CREATED)


class MovieDetailAPIView(APIView):
    def get_object(self, id):
        try:
            return Movie.objects.get(id=id)
        except Movie.DoesNotExist:
            return None

    def get(self, request, id):
        movie = self.get_object(id)
        if not movie:
            return Response({'error': 'Фильм не найден'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data=MovieSerializer(movie).data)

    def put(self, request, id):
        movie = self.get_object(id)
        if not movie:
            return Response({'error': 'Фильм не найден'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MovieValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        for key, value in serializer.validated_data.items():
            setattr(movie, key, value)
        movie.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        movie = self.get_object(id)
        if not movie:
            return Response({'error': 'Фильм не найден'}, status=status.HTTP_404_NOT_FOUND)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewListAPIView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        data = ReviewSerializer(reviews, many=True).data
        return Response(data={'list': data})

    def post(self, request):
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        review = Review.objects.create(**serializer.validated_data)
        return Response(data=ReviewSerializer(review).data, status=status.HTTP_201_CREATED)


class ReviewDetailAPIView(APIView):
    def get_object(self, id):
        try:
            return Review.objects.get(id=id)
        except Review.DoesNotExist:
            return None

    def get(self, request, id):
        review = self.get_object(id)
        if not review:
            return Response({'error': 'Отзыв не найден'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data=ReviewSerializer(review).data)

    def put(self, request, id):
        review = self.get_object(id)
        if not review:
            return Response({'error': 'Отзыв не найден'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        for key, value in serializer.validated_data.items():
            setattr(review, key, value)
        review.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        review = self.get_object(id)
        if not review:
            return Response({'error': 'Отзыв не найден'}, status=status.HTTP_404_NOT_FOUND)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# def director_list_api_view(request):
#     print(request.user)
#     if request.method == 'GET':
#         directors = Director.objects.all()
#         data = DirectorSerializer(directors, many=True).data
#         return Response(data={'list': data})
#     elif request.method == 'POST':
#         #Validation
#         serializer = DirectorValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST,
#                             data=serializer.errors)
#         print(request.data)
#         print(serializer.validated_data)
#
#         name = serializer.validated_data.get('name')
#         #Create
#         director = Director.objects.create(
#             name= name
#         )
#         return Response(data= DirectorSerializer(director).data,
#                         status=status.HTTP_201_CREATED)
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def director_detail_api_view(request, id):
#     try:
#         director = Director.objects.get(id=id)
#     except Director.DoesNotExist:
#         return Response({'error': 'Режиссер не найден'}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         data = DirectorSerializer(director).data
#         return Response(data=data)
#     #Create
#     elif request.method == 'PUT':
#     # Validation
#         serializer = DirectorValidateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         director.name = serializer.validated_data.get('name')
#         director.save()
#         return Response(status=status.HTTP_201_CREATED)
#     #Delete
#     elif request.method == 'DELETE':
#         director.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#


# @api_view(['GET', 'POST'])
# def movie_list_api_view(request):
#     if request.method == 'GET':
#         movie = (Movie.objects.
#               prefetch_related('review').all())
#         data = MovieSerializer(movie, many=True).data
#         return Response(data={'list': data})
#     elif request.method == 'POST':
#         serializer = MovieValidateSerializer(data=request.data)
#         if not serializer.is_valid() :
#             return Response(status=status.HTTP_400_BAD_REQUEST,
#                             data=serializer.errors)
#         print(request.data)
#         print(serializer.validated_data)
#
#         title = serializer.validated_data.get('title')
#         description = serializer.validated_data.get('description')
#         duration = serializer.validated_data.get('duration')
#         director_id = serializer.validated_data.get('director_id')
#
#         movie = Movie.objects.create(
#             title= title,
#             description = description,
#             duration = duration,
#             director_id = director_id
#         )
#         return Response(data=MovieSerializer(movie).data,
#                         status=status.HTTP_201_CREATED)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_detail_api_view(request, id):
#     try:
#         movie = Movie.objects.get(id=id)
#     except Movie.DoesNotExist:
#         return Response({'error': 'Фильм не найден'}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         data = MovieSerializer(movie).data
#         return Response(data=data)
#     elif request.method == 'PUT':
#         serializer = MovieValidateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         movie.title = serializer.validated_data.get('title')
#         movie.description = serializer.validated_data.get('description')
#         movie.duration = serializer.validated_data.get('duration')
#         movie.director_id = serializer.validated_data.get('director_id')
#         movie.save()
#         return Response(status=status.HTTP_201_CREATED)
#     elif request.method == 'DELETE':
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
#
#
# @api_view(['GET', 'POST'])
# def review_list_api_view(request):
#     if request.method == 'GET':
#         reviews = Review.objects.all()
#         data = ReviewSerializer(reviews, many=True).data
#         return Response(data={'list': data})
#     elif request.method == 'POST':
#         serializer = ReviewValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST,
#                             data=serializer.errors)
#         print(request.data)
#         print(serializer.validated_data)
#         stars = serializer.validated_data.get('stars')
#         text = serializer.validated_data.get('text')
#         movie_id = serializer.validated_data.get('movie_id')
#
#         review = Review.objects.create(
#             stars= stars,
#             text= text,
#             movie_id= movie_id
#         )
#         return Response(data=ReviewSerializer(review).data,
#                         status=status.HTTP_201_CREATED)
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def review_detail_api_view(request, id):
#     try:
#         review = Review.objects.get(id=id)
#     except Review.DoesNotExist:
#         return Response({'error': 'Отзыв не найден'}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         data = ReviewSerializer(review).data
#         return Response(data=data)
#
#     elif request.method == 'PUT':
#         serializer = ReviewValidateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         review.stars =  serializer.validated_data.get('stars')
#         review.text = serializer.validated_data.get('text')
#         review.movie_id = serializer.validated_data.get('movie_id')
#         review.save()
#         return Response(status=status.HTTP_201_CREATED)
#
#     elif request.method == 'DELETE':
#         review.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)