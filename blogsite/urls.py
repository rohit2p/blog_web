from django.contrib import admin
from django.urls import path, include
from blogsite import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('post/', views.post_create, name='post_create'),
    path('post/<int:id>/', views.single_post, name='single'),  # Single post detail
    path('reg/', views.reg_task, name='register'),
    path('login/', views.login_task, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('post/update/<int:id>/', views.update_post, name='update_post'),
    path('post/delete/<int:id>/', views.delete_post, name='delete_post'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

