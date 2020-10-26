from django.urls import include, path
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/new/', views.PostNew.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', views.PostEdit.as_view(), name='post_edit'),
    path('post/feedback/', views.FeedbackView.as_view(), name='feedback'),
    path('post/seefeedback/', views.SeeFeedback.as_view(template_name='blog/list_feedback.html'), name='see_feedback'),
    path('post/<int:pk>/delete/', views.PostDelete.as_view(), name='delete'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]