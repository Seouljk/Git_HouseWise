from django.urls import path
from . import views

urlpatterns = [
    path("housewise/", views.login_view, name="login"),
    path("housewise/logout/", views.logout_view, name="logout"),
    path("housewise/<str:username>/menu/", views.menu_view, name="menu"),
    path("housewise/<str:username>/menu/user/", views.user_list, name="user"), 
    path('housewise/user_login_sessions/', views.user_login_sessions, name='user_login_sessions'),  # Add this line
    path("housewise/<str:username>/menu/materials/", views.material_view, name="materials"),
    path("housewise/<str:username>/menu/feedbacks/", views.feedbacks_view, name="feedbacks"),
    path("housewise/<str:username>/profile/", views.profile_view, name="profile_view"),
    path("housewise/<str:username>/profile/save/", views.save_profile_changes, name='save_profile_changes'),
    path("housewise/<str:username>/scripts/", views.script_view, name="scripts"),
]