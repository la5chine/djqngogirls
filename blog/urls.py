from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(template_name='blog/post_list.html'), name='post_list'),
    path('post/<int:pk>/', views.PostDetail.as_view(template_name='blog/post_detail.html'), name='post_detail'),
    path('post/new/', views.PostEdit.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', views.PostEdit.as_view(), name='post_edit'),
    path('post/feedback/', views.FeedbackView.as_view(), name='feedback'),
    path('post/seefeedback/', views.SeeFeedback.as_view(template_name='blog/list_feedback.html'), name='see_feedback'),

]