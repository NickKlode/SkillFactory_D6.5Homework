from django.urls import path, include
from .views import *

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewsDetail.as_view(), name='detail'),
    path('search/', Search.as_view(), name='search'),
    path('create/', CreatePost.as_view(), name='create'),
    path('<int:pk>/update/', UpdatePost.as_view(), name='update'),
    path('<int:pk>/delete/', DeletePost.as_view(), name='delete'),
    path('categories/', CategoryList.as_view(), name='categories'),
    path('categories/<int:pk>', OneCategory.as_view(), name='category'),
    path('categories/<int:pk>/subscribe/', add_subscriber, name='subscribe'),
]
