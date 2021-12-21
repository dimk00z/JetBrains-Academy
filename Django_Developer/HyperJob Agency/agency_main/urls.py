from django.urls import path
from django.views.generic import RedirectView
from resume.views import CreateResumeView
from vacancy.views import CreateVacancyView

from .views import HomeView, LoginPageView, MainPageView, SingupView

urlpatterns = [
    path("", MainPageView.as_view()),
    path("login/", RedirectView.as_view(url="/login")),
    path("signup/", RedirectView.as_view(url="/signup")),
    path("login", LoginPageView.as_view()),
    path("signup", SingupView.as_view()),
    path("home", HomeView.as_view()),
    path("resume/new", CreateResumeView.as_view()),
    path("vacancy/new", CreateVacancyView.as_view()),
]
