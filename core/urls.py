# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('deactivate/', views.deactivate_account, name='deactivate_account'),
    path('delete/', views.delete_account, name='delete_account'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('chat/<int:user_id>/', views.start_chat, name='start_chat'),
    path('search/', views.search_users, name='search_users'),
    path('profile/update/', views.profile_update, name='profile_update'),
]
