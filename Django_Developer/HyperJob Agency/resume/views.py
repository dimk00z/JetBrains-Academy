from django import forms
from django.http import HttpResponse
from django.views.generic import CreateView, TemplateView
from resume.models import Resume


class ResumeListView(TemplateView):
    template_name = "resumes_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        resumes = Resume.objects.all()
        context["resumes"] = resumes
        return context


class CreateResumeForm(forms.Form):
    description = forms.CharField(max_length=1024)


class CreateResumeView(CreateView):
    model = Resume
    template_name = "create_resume.html"
    fields = ["description"]
    success_url = "/resumes"

    def get(self, request):
        if request.user.is_authenticated:
            return super().get(request=request)
        return HttpResponse(status=403)

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super(CreateResumeView, self).form_valid(form)
