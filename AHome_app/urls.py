from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import HomePageView, DesignListView, DesignDeleteView, DesignDetailView, DesignUpdateView, DesignCreateView, UnfollowUserView, CommentDeleteView, CommentUpdateView, LikeDesignView, FollowUserView, OverlayLogView, CameraFilterView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('designs/', DesignListView.as_view(), name='design-list'),
    path('design/<int:pk>/', DesignDetailView.as_view(), name='design-detail'),
    path('design/new/', DesignCreateView.as_view(), name='design-create'),
    path('designs/<int:pk>/edit/', DesignUpdateView.as_view(), name='design-update'),
    path('designs/<int:pk>/delete/', DesignDeleteView.as_view(), name='design-delete'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment-edit'),
    path('design/<int:pk>/like/', LikeDesignView.as_view(), name='like-design'),
    path('user/<int:pk>/follow/', FollowUserView.as_view(), name='follow-user'),
    path('user/<int:pk>/unfollow/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('design/<int:pk>/overlay-log/', OverlayLogView.as_view(), name='overlay-log'),
    path('camera-filter/', CameraFilterView.as_view(), name='camera-filter'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)