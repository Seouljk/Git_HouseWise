from django.db import models
from django.utils import timezone  # For auto-setting login date and time
from django.contrib.auth.hashers import make_password  # For password hashing

class UserType(models.Model):
    userTypeID = models.AutoField(primary_key=True)
    userType = models.CharField(max_length=50)  # Admin or User
    status = models.BooleanField(default=True)  # Active or Inactive

    def __str__(self):
        return f"{self.userType} ({'Active' if self.status else 'Inactive'})"


class User(models.Model):
    userID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)  # Length for hashed password
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    user_type = models.OneToOneField(UserType, on_delete=models.CASCADE, related_name="user")

    def save(self, *args, **kwargs):
        if not self.pk:  # Only hash password on creation
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    def is_active(self):
        # Check if the user has any active login sessions
        return self.login_sessions.filter(loginDateandTime__date=timezone.now().date()).exists()

    def __str__(self):
        return self.username


class LoginSession(models.Model):
    loginSessionId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="login_sessions")
    loginDuration = models.DurationField()  # Tracks duration in time format
    loginDateandTime = models.DateTimeField(default=timezone.now)  # Auto-set to current time

    def __str__(self):
        return f"{self.user.username} - {self.loginDuration} ({self.loginDateandTime})"
