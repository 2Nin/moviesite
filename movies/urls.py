from django.urls import path

from . import views

app_name = 'movies'
urlpatterns = [
    path('<int:movie_id>/', views.detail_movie, name='detail'),
    path('', views.list_movies, name='index'),
    path('search/', views.search_movies, name='search'),
    path('create/', views.create_movie, name='create')
]