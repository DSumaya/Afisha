from django.urls import path


from users import views

urlpatterns = [
    path('registration/', views.RegisterView.as_view(), name='register'),
    path('authorization/', views.AuthAPIView.as_view(), name ='auth'),
    path('confirm/', views.ConfirmUserAPIView.as_view(), name= 'confirm'),

]

