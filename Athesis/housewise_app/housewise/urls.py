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
    path('housewise/user_login_sessions/', views.user_login_sessions, name='user_login_sessions'), 
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

#SCRIPT:
    path("housewise/<str:username>/scripts/", views.script_view, name="scripts"),
]