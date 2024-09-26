from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,  HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.views.generic import TemplateView

from .models import User

class LoginView(TemplateView):
    template_name = "housewise/login.html"


class MenuView(TemplateView):
    template_name = "housewise/menu.html"

class UserView(TemplateView):
    template_name = "housewise/user.html"

class MaterialView(TemplateView):
    template_name = "housewise/materials.html"

class FeedbacksView(TemplateView):
    template_name = "housewise/feedbacks.html"

class ScriptView(TemplateView):
    template_name = "housewise/scripts.html"

class ProfileView(TemplateView):
    template_name = "housewise/profile.html"

class IndexView(generic.ListView):
    model = User
    template_name = "housewise/index.html"
    context_object_name = "user_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return User.objects.order_by("-username")[:5]


#def index(request):
#    users = User.objects.order_by('-username')[:5]
#    context = {
#        'user_list':users
#    }
#    return render(request, 'housewise/index.html', context)  
    #output = ', '.join ([u.username for u in user])
    #return HttpResponse(output)

class DetailView(generic.DetailView):
    model = User
    template_name = 'housewise/detail.html'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return User.objects.get(username=username)

#def detail(request, username):
#    users = get_object_or_404(User, username=username)
#    detailcontext = {
#        'name' : users.name,
#        'username': users.username,
#        'email': users.email,
#        'age': users.age,
#    }
#    return render(request, 'housewise/detail.html', detailcontext)  