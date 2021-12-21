from django.urls import path

from .views import ResumeListView

urlpatterns = [
    path("", ResumeListView.as_view()),
]
