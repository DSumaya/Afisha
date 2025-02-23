from django.urls import path
from movie_app import views

urlpatterns = [
    path('director/', views.DirectorListAPIView.as_view(), name='director-list'),
    path('director/<int:id>/', views.DirectorDetailAPIView.as_view(), name='director-detail'),

    path('movie/', views.MovieListAPIView.as_view(), name='movie-list'),
    path('movie/<int:id>/', views.MovieDetailAPIView.as_view(), name='movie-detail'),

    path('review/', views.ReviewListAPIView.as_view(), name='review-list'),
    path('review/<int:id>/', views.ReviewDetailAPIView.as_view(), name='review-detail'),

]