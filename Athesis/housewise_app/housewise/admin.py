from django.contrib import admin
from django.contrib.auth.hashers import make_password

from .models import UserHousewise
from .models import UserType
from .models import LoginSession
from .models import HouseType
from .models import Project
from .models import HouseType
from .models import Roof
from .models import Rooms
from .models import CR
from .models import Materials
from .models import MaterialPrice
from .models import Feedback
from .models import FeedbackComment

class UserHousewiseAdmin(admin.ModelAdmin):
    # Overriding log_change to prevent logging admin changes
    def log_change(self, request, obj, message):
        pass  # This will prevent admin log entries for changes

    def save_model(self, request, obj, form, change):
        # Hash the password if it was changed
        if 'password' in form.changed_data:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(UserHousewise, UserHousewiseAdmin)
admin.site.register(UserType)
admin.site.register(LoginSession)
admin.site.register(HouseType)
admin.site.register(Project)
admin.site.register(Roof)
admin.site.register(Rooms)
admin.site.register(CR)
admin.site.register(Materials)
admin.site.register(MaterialPrice)
admin.site.register(Feedback)
admin.site.register(FeedbackComment)