from django.urls import path, re_path
from github import views

urlpatterns = [
    path('tweets-list/', views.TweetsListView.as_view(), name='tweets_list'),

]
