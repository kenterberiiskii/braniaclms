from mainapp import views
from django.urls import path
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path('courses/', views.CoursesView.as_view(), name='courses'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('docsite/', views.DocSiteView.as_view(), name='docsite'),
    path('', views.IndexView.as_view(), name='index'),
    # path('/', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    # path('news/', views.NewsView.as_view(), name='news'),
    # path('news/<pk>/', views.NewsDetail.as_view(), name='news_detail'),
    path('news/', views.NewsListView.as_view(), name='news'),
    path('news/add/', views.NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/update/', views.NewsUpdateView.as_view(), name='news_update'),
    path('news/<int:pk>/detail/', views.DetailView.as_view(), name='news_detail'),
    path('news/<int:pk>/delete/', views.DeleteView.as_view(), name='news_delete'),
]

