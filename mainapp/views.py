# from django.shortcuts import render
import json

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DetailView, CreateView, DeleteView
from datetime import datetime
from django.shortcuts import get_object_or_404
from mainapp.models import News


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
    paginate_by = 5

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