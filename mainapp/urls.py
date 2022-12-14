from django.views.decorators.cache import cache_page

from mainapp import views
from django.urls import path
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    # path('courses/', views.CoursesView.as_view(), name='courses'),
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
    path('news/<int:pk>/detail/', views.NewsDetailView.as_view(), name='news_detail'),
    path('news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),
    # path("courses/", views.CoursesListView.as_view(), name="courses"),
    path("courses/",cache_page(60 * 5)(views.CoursesListView.as_view()), name="courses",),
    path("courses/<int:pk>/",views.CoursesDetailView.as_view(),name="courses_detail"),
    path("course_feedback/",views.CourseFeedbackFormProcessView.as_view(),name="course_feedback"),
    path("log_view/", views.LogView.as_view(), name="log_view"),
    path("log_download/", views.LogDownloadView.as_view(), name="log_download"),
]

