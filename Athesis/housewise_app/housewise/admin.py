from django.contrib import admin

from .models import User
from .models import UserType
from .models import LoginSession

admin.site.register(User)
admin.site.register(UserType)
admin.site.register(LoginSession)