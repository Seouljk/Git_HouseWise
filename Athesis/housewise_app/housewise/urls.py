from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("housewise/", views.login_view, name="login"),
    path("housewise/logout/", views.logout_view, name="logout"),
    path("housewise/<str:username>/menu/", views.menu_view, name="menu"),
    path("housewise/<str:username>/menu/user/", views.user_list, name="user"), 
    path('housewise/api/dashboard-data/', views.dashboard_data_api, name='dashboard_data_api'),
    path("housewise/login_sessions/", views.user_login_sessions, name="user_login_sessions"),
    path('housewise/user_feedbacks/', views.user_feedbacks, name='user_feedbacks'),
    path('housewise/api/graph-data/', views.graph_data_api, name='graph_data_api'),
    path('housewise/api/feedbacks/', views.feedback_list_api, name='feedback_list_api'),
    path('housewise/delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path("housewise/<str:username>/menu/materials/", views.material_view, name="materials"),
    path('housewise/get_material_prices/', views.get_material_prices, name='get_material_prices'),
    path("housewise/<str:username>/menu/feedbacks/", views.feedbacks_view, name="feedbacks"),
    path("housewise/<str:username>/profile/", views.profile_view, name="profile_view"),
    path("housewise/<str:username>/profile/save/", views.save_profile_changes, name='save_profile_changes'),


#EMAIL 
    path('housewise/api/send_verification_code/', views.send_verification_code, name='send_verification_code'),
    path('housewise/api/verify_code/', views.verify_code, name='verify_code'),
    path('housewise/api/check_email/', views.check_email, name='check_email'),
    path('housewise/api/check_username/', views.check_username, name='check_username'),


#MOBILE APP URLS

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('housewise/auth/login/', views.login_user, name='login_user'),
    path('housewise/update_user/', views.update_user, name='update_user'),
    path('housewise/api/logout/', views.logout_user, name='logout_user'),
    path('housewise/api/create_user_account/', views.create_user_account, name='create_user_account'),
    path('housewise/api/set-profile-icon/', views.set_profile_icon, name='set_profile_icon'),
    path('housewise/api/get-profile-icon/', views.get_profile_icon, name='get_profile_icon'),
    path('housewise/api/published-projects/', views.published_projects_view, name='published-projects'),
    path('housewise/api/projects/<int:project_id>/toggle-like/', views.toggle_like, name='toggle_like'),
    path('housewise/api/user-owned-projects/', views.user_owned_projects_view, name='user-owned-projects'),
    path('housewise/api/projects/<int:pk>/toggle-publish/', views.toggle_project_publish_status, name='toggle-project-publish'),
    path('housewise/api/create_project/', views.create_project, name='create_project'),
    path('housewise/api/projects/<int:project_id>/delete/', views.delete_project, name='delete_project'),
    path('housewise/api/projects/<int:project_id>/feedback/', views.save_feedback, name='save_feedback'),
    path('housewise/api/projects/<int:project_id>/get-feedback/', views.get_feedback, name='get_feedback'),
    path('housewise/api/liked-projects/', views.liked_projects_view, name='liked_projects_view'),
    path('housewise/api/forgot_password_username/', views.forgot_password_username, name='forgot_password_username'),
    path('housewise/api/send_reset_code/', views.send_reset_code, name='send_reset_code'),
    path('housewise/api/reset_password/', views.reset_password, name='reset_password'),
    path('housewise/api/resetverify_code/', views.resetverify_code, name='resetverify_code'),
    path('housewise/api/session/', views.session_status, name='session_status'),
    path('housewise/api/get_material_prices/', views.get_material_prices, name='get_material_prices'),



#SCRIPT:
    path("housewise/<str:username>/scripts/", views.script_view, name="scripts"),
]