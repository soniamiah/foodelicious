from . import views
from django.urls import path, include
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)
urlpatterns = [
    path('', views.home, name='blog-home'),
    path('rating/', views.rate),
    path('getRating/<int:recipeId>', views.getRating),
    path('results/', views.results, name='blog-results'),
    path('ingredients/', views.result_ing, name='blog-ingredients'),
    path('random/', views.random, name='blog-random'),
    path('info/<int:id>', views.info, name='blog-info'),
    path('post/', PostListView.as_view(), name='blog-post'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('recommendation', views.user_recommendation_list, name= 'user_recommendation_list'),

]
