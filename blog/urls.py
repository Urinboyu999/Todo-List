from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('todo_delete/<int:pk>/', views.detail_todo, name='detail_todo'),
    path('todo_complete/<int:pk>/', views.complete_todo, name='complete_todo'),

    # Reg, log va logoutlar url lari

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]