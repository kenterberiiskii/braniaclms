# from django.shortcuts import render
import json

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.http import HttpResponse, FileResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView, DetailView, CreateView, DeleteView
from datetime import datetime
from django.shortcuts import get_object_or_404

from mainapp import forms as mainapp_forms
from mainapp.forms import CourseFeedbackForm
from mainapp.models import News, Course, Lesson, CourseTeacher, CourseFeedback

from django.http import JsonResponse
from mainapp import forms as mainapp_forms
from mainapp import models as mainapp_models
from django.template.loader import render_to_string

from django.contrib import messages
from django.http.response import HttpResponseRedirect
from mainapp import tasks as mainapp_tasks


# Create your views here.

class ContactsView(TemplateView):
    template_name = 'mainapp/contacts.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['contacts'] = [
            {
                'map': 'https://yandex.ru/maps/org/petropavlovskaya_krepost/146720535721/?utm_medium=mapframe&utm_source=maps',
                'city': 'SPB',
                'phone': '1111111111',
                'email': '12121213@dfdfddf.ru',
                'adress': 'Street',
            },
            {
                'map': 'https://yandex.ru/maps/org/petropavlovskaya_krepost/146720535721/?utm_medium=mapframe&utm_source=maps',
                'city': 'SPB2',
                'phone': '1222222',
                'email': '22222223@dfdfddf.ru',
                'adress': 'Street2',
            }
        ]
        return context_data

class CoursesView(TemplateView):
    template_name = 'mainapp/courses_list.html'

class DocSiteView(TemplateView):
    template_name = 'mainapp/doc_site.html'


class IndexView(TemplateView):
    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'some title'
        return context_data

class LoginView(TemplateView):
    template_name = 'mainapp/login.html'


# class NewsView(TemplateView):
#     template_name = 'mainapp/news.html'
#
#     # def openjson(self):
#     #     with open('static/json/my.json', 'r') as f:
#     #         my_json_obj = json.load(f)
#     #     return my_json_obj
#
#     def get_context_data(self, **kwargs):
#         context_data = super().get_context_data(**kwargs)
#         # context_data['object_list'] = self.openjson()
#         context_data['object_list'] = News.objects.filter(deleted=False)
#         return context_data


class NewsListView(ListView):
    model = News
    paginate_by = 2

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class NewsDetailView(DetailView):
    model = News

class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = News
    fields = '__all__'
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.add_news',)



class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = News
    fields = '__all__'
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.change_news',)


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.delete_news',)

class NewsDetail(TemplateView):
    template_name = 'mainapp/news_detail_old.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object'] = get_object_or_404(News, pk=self.kwargs.get("pk"))
        return context_data


class CoursesListView(TemplateView):
    template_name = "mainapp/courses_list.html"
    def get_context_data(self, **kwargs):
        context = super(CoursesListView, self).get_context_data(**kwargs)
        context["objects"] = mainapp_models.Course.objects.all()[:7]
        return context

class CoursesDetailView(TemplateView):
    template_name = "mainapp/courses_detail.html"
    def get_context_data(self, pk=None, **kwargs):
        context = super(CoursesDetailView, self).get_context_data(**kwargs)
        context["course_object"] = get_object_or_404(mainapp_models.Course, pk=pk)
        context["lessons"] = mainapp_models.Lesson.objects.filter(course=context["course_object"])
        context["teachers"] = mainapp_models.CourseTeacher.objects.filter(courses=context["course_object"])
        if not self.request.user.is_anonymous:
            if not mainapp_models.CourseFeedback.objects.filter(course=context["course_object"], user=self.request.user).count():
                context["feedback_form"] = mainapp_forms.CourseFeedbackForm(course=context["course_object"], user=self.request.user)
                context["feedback_list"] = mainapp_models.CourseFeedback.objects.filter(course=context["course_object"]).order_by("-created", "-rating")[:5]

        cached_feedback = cache.get(f"feedback_list_{pk}")
        if not cached_feedback:
            context["feedback_list"] = (mainapp_models.CourseFeedback.objects.filter(course=context["course_object"]).order_by("-created", "-rating")[:5].select_related())
            cache.set(f"feedback_list_{pk}", context["feedback_list"], timeout=300)
        else:
            context["feedback_list"] = cached_feedback
        return context

class CourseFeedbackFormProcessView(LoginRequiredMixin, CreateView):
    model = mainapp_models.CourseFeedback
    form_class = mainapp_forms.CourseFeedbackForm
    def form_valid(self, form):
        self.object = form.save()
        rendered_card = render_to_string("mainapp/includes/feedback_card.html", context={"item": self.object})
        return JsonResponse({"card": rendered_card})

class LogView(TemplateView):
    template_name = "mainapp/log_view.html"
    def get_context_data(self, **kwargs):
        context = super(LogView, self).get_context_data(**kwargs)
        log_slice = []
        with open(settings.LOG_FILE, "r") as log_file:
            for i, line in enumerate(log_file):
                if i == 1000: # first 1000 lines
                    break
                log_slice.insert(0, line) # append at start
            context["log"] = "".join(log_slice)
        return context

class LogDownloadView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser
    def get(self, *args, **kwargs):
        return FileResponse(open(settings.LOG_FILE, "rb"))


class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"
    def get_context_data(self, **kwargs):
        context = super(ContactsPageView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["form"] = mainapp_forms.MailFeedbackForm(user=self.request.user)
        return context
    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            cache_lock_flag = cache.get(f"mail_feedback_lock_{self.request.user.pk}")
            if not cache_lock_flag:
                cache.set(f"mail_feedback_lock_{self.request.user.pk}","lock",timeout=300,)
                messages.add_message(self.request, messages.INFO,("Message sended"))
                mainapp_tasks.send_feedback_mail.delay(
                    {"user_id": self.request.POST.get("user_id"),"message": self.request.POST.get("message"),}
                )
            else:
                messages.add_message(self.request,messages.WARNING,("You can send only one message per 5 minutes"),)
        return HttpResponseRedirect(reverse_lazy("mainapp:contacts"))