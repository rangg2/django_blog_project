from django.urls import path, include
from . import views
import blog_app.views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.post_list, name="board"),
    path("post/<int:post_id>", views.post_page, name="post"),
    path('post_list/<str:topic>/', views.post_list, name='post_list_by_topic'),
    path("login/", blog_app.views.custom_login, name="login"),
    path("signup/", blog_app.views.signup, name="signup"),
    path("logout/", blog_app.views.logout, name="logout"),
    path('write/', views.create_or_update_post, name='create_or_update_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('edit_post/<int:post_id>/', views.create_or_update_post, name='create_or_update_post'),
    path('api/blog_posts/', views.BlogPostList.as_view(), name='blogpost-list'),
    path("failed/", blog_app.views.signup, name="failed"),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('image-upload/', views.image_upload.as_view(), name='image_upload'),
]
