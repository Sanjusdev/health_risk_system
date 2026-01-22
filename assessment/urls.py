from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Assessments
    path('assessment/new/', views.new_assessment, name='new_assessment'),
    path('assessment/<int:pk>/result/', views.assessment_result, name='assessment_result'),
    path('assessment/<int:pk>/', views.assessment_detail, name='assessment_detail'),
    path('assessment/history/', views.assessment_history, name='assessment_history'),
    
    # Profile
    path('profile/', views.profile_view, name='profile'),
    
    # Goals
    path('goals/', views.goals_list, name='goals_list'),
    path('goals/create/', views.goal_create, name='goal_create'),
    path('goals/<int:pk>/edit/', views.goal_edit, name='goal_edit'),
    path('goals/<int:pk>/delete/', views.goal_delete, name='goal_delete'),
    
    # API
    path('api/assessment-data/', views.api_assessment_data, name='api_assessment_data'),
]
