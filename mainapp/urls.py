from mainapp import views
from django.urls import path
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path('courses/', views.CoursesView.as_view()),
    path('contacts/', views.ContactsView.as_view()),
    path('docsite/', views.DocSiteView.as_view()),
    path('', views.IndexView.as_view()),
    path('/', views.IndexView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('news/', views.NewsView.as_view()),
]