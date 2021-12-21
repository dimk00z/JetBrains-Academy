from django.http import HttpResponse
from django.views.generic import CreateView, TemplateView
from vacancy.models import Vacancy


class VacancyMainView(TemplateView):
    template_name = "vacancy_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancies = Vacancy.objects.all()
        context["vacancies"] = vacancies
        return context


class CreateVacancyView(CreateView):
    model = Vacancy
    template_name = "create_vacancy.html"
    fields = ["description"]
    success_url = "/vacancies"

    def get(self, request):
        print(request.user.is_staff)
        if request.user.is_authenticated:
            if request.user.is_staff:
                return super().get(request=request)
        return HttpResponse(status=403)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return super().post(request=request)
        return HttpResponse(status=403)

    def form_valid(self, form):

        form.instance.author = self.request.user

        return super(CreateVacancyView, self).form_valid(form)
