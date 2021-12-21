from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views import View
from django.views.generic import CreateView, TemplateView


class MainPageView(TemplateView):
    template_name = "agency_index.html"


class LoginPageView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'


class SingupView(CreateView):
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'signup.html'


class HomeView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login')
        if not request.user.is_staff:
            return redirect('/resume/new')
        else:
            return redirect('/vacancy/new')
