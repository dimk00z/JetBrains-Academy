from django.urls import path

from .views import VacancyMainView

urlpatterns = [
    path("", VacancyMainView.as_view()),
]
