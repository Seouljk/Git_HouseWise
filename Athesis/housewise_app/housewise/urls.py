from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("housewise-admin.up.railway.app/", views.login_view, name="login"), 
    path("housewise-admin.up.railway.app/logout/", views.logout_view, name="logout"),
    path("housewise-admin.up.railway.app/<str:username>/menu/", views.menu_view, name="menu"),
    path("housewise-admin.up.railway.app/<str:username>/menu/user/", views.user_list, name="user"), 
    path('housewise-admin.up.railway.app/user_login_sessions/', views.user_login_sessions, name='user_login_sessions'),  # Add this line
    path("housewise-admin.up.railway.app/<str:username>/menu/materials/", views.material_view, name="materials"),
    path('housewise-admin.up.railway.app/get_material_prices/', views.get_material_prices, name='get_material_prices'),
    path("housewise-admin.up.railway.app/<str:username>/menu/feedbacks/", views.feedbacks_view, name="feedbacks"),
    path("housewise-admin.up.railway.app/<str:username>/profile/", views.profile_view, name="profile_view"),
    path("housewise-admin.up.railway.app/<str:username>/profile/save/", views.save_profile_changes, name='save_profile_changes'),


#MOBILE APP URLS
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('housewise-admin.up.railway.app/auth/login/', views.login_user, name='login_user'),
    path('housewise-admin.up.railway.app/update_user/', views.update_user, name='update_user'),

#SCRIPT:
    path("housewise-admin.up.railway.app/<str:username>/scripts/", views.script_view, name="scripts"),
]