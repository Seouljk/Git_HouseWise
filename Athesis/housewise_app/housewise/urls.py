from django.urls import path, include
from . import views
from django.views.generic.base import RedirectView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("", RedirectView.as_view(url="/housewise/", permanent=False)),  # Redirect root to /housewise/
    path("housewise/", include(([
        path("", views.login_view, name="login"),
        path("logout/", views.logout_view, name="logout"),
        path("<str:username>/menu/", views.menu_view, name="menu"),
        path("<str:username>/menu/user/", views.user_list, name="user"), 
        path('user_login_sessions/', views.user_login_sessions, name='user_login_sessions'), 
        path("<str:username>/menu/materials/", views.material_view, name="materials"),
        path('get_material_prices/', views.get_material_prices, name='get_material_prices'),
        path("<str:username>/menu/feedbacks/", views.feedbacks_view, name="feedbacks"),
        path("<str:username>/profile/", views.profile_view, name="profile_view"),
        path("<str:username>/profile/save/", views.save_profile_changes, name='save_profile_changes'),


    #MOBILE APP URLS
        path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('auth/login/', views.login_user, name='login_user'),
        path('update_user/', views.update_user, name='update_user'),

    #SCRIPT:
        path("<str:username>/scripts/", views.script_view, name="scripts"),
]
, 'housewise'))),
]