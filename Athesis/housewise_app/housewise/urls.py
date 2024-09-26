from django.urls import path

from . import views

urlpatterns = [
    path("", views.LoginView.as_view(), name="login"),

    path("<str:username>/", views.DetailView.as_view(), name="detail"),

    path("menu", views.MenuView.as_view(), name="menu"),

    path("menu/user", views.UserView.as_view(), name="user"),

    path("menu/materials", views.MaterialView.as_view(), name="materials"),

    path("menu/feedbacks", views.FeedbacksView.as_view(), name="feedbacks"),

    path("profile", views.ProfileView.as_view(), name="profile"),

    path("scripts", views.ScriptView.as_view(), name="scripts"),

]