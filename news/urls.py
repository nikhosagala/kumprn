from django.urls import path

from news import views

app_name = 'news'

urlpatterns = [
    path('tags/', views.TagList.as_view(), name='tag-list'),
    path('tags/<slug>/', views.TagDetail.as_view(), name='tag-detail'),
]
