from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('project/<int:pk>/task/new/', views.TaskCreateView.as_view(), name='task_create'),
    path('project/<int:pk>/task/<int:task_pk>/edit/', views.TaskUpdateView.as_view(), name='task_edit'),
]
