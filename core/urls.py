from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api1'

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
    path('aside/', views.AsideAPIView.as_view(), name='aside'),
    path('feedback/', views.FeedBackAPIView.as_view()),
    path('registration/', views.RegistrationAPIView.as_view()),
    path('profile/', views.ProfileAPIView.as_view()),
    path("comments/", views.CommentView.as_view()),
    path("comments/<slug:post_slug>/", views.CommentView.as_view()),
    path("comments/delete/<int:pk>", views.CommentDestroy.as_view()),
]
