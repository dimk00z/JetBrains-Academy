from django.urls import path

from .views import MainPageView, NewsView, NewsMainView, CreateNewsView

urlpatterns = [
    path('', MainPageView.as_view()),
    path('news/', NewsMainView.as_view()),
    path('news/create/', CreateNewsView.as_view()),
    path('news/<str:news_id>/', NewsView.as_view()),
]
