# from django.shortcuts import render
import json
from django.http import HttpResponse
from django.views.generic import TemplateView
from datetime import datetime

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

class NewsView(TemplateView):
    template_name = 'mainapp/news.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data['object_list'] = [
            {
                'title': 'Новость 1',
                'preview': 'Предварительное описание новости 1',
                'data': datetime.now()
            },
            {
                'title': 'Новость 2',
                'preview': 'Предварительное описание новости 2',
                'data': datetime.now()
            },
            {
                'title': 'Новость 3',
                'preview': 'Предварительное описание новости 3',
                'data': datetime.now()
            },
            {
                'title': 'Новость 4',
                'preview': 'Предварительное описание новости 4',
                'data': datetime.now()
            },
            {
                'title': 'Новость 5',
                'preview': 'Предварительное описание новости 5',
                'data': datetime.now()
            },
        ]
        return context_data



