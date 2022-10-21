from mainapp import views
from django.urls import path
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path('courses/', views.CoursesView.as_view(), name='courses'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('docsite/', views.DocSiteView.as_view(), name='docsite'),
    path('', views.IndexView.as_view(), name=''),
    path('/', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('my_news/', views.NewsView.as_view(), name='news'),
]