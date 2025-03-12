from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password, is_password_usable
from django.contrib import admin
from datetime import date


class UserType(models.Model):
    usertype_id = models.AutoField(primary_key=True)
    user_type = models.CharField(max_length=50)  # Admin or User
    status = models.BooleanField(default=True)  # Active or Inactive

    def __str__(self):
        return f"{self.user_type} ({'Active' if self.status else 'Inactive'})"
    

class UserHousewiseManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # Use the built-in method for password hashing
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

         # Ensure a user type is set (assuming Admin is represented by 'admin')
        if 'user_type' not in extra_fields:
            admin_usertype = UserType.objects.filter(user_type='admin').first()
            if not admin_usertype:
                raise ValueError("Admin user type must exist in UserType table.")
            extra_fields['user_type'] = admin_usertype  # Use the UserType instance, not usertype_id

        return self.create_user(username, email, password, **extra_fields)
    

class UserHousewise(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE, related_name="user")
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_staff = models.BooleanField(default=False)  # Change to a regular field
    is_active = models.BooleanField(default=True)
    profile_icon = models.CharField(max_length=255, null=True, blank=True, default=27)  # Default icon path

    objects = UserHousewiseManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # Add any other fields that are required

    def save(self, *args, **kwargs):
        # Only hash the password if it's not usable (i.e., not already hashed)
        if not is_password_usable(self.password):
            self.password = make_password(self.password)

        if self.birthdate:
            today = date.today()
            self.age = today.year - self.birthdate.year - (
                (today.month, today.day) < (self.birthdate.month, self.birthdate.day)
            )

        super(UserHousewise, self).save(*args, **kwargs)

    def check_password(self, password):
        return check_password(password, self.password)

    def __str__(self):
        return self.username


class LoginSession(models.Model):
    loginsession_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserHousewise, on_delete=models.CASCADE, related_name="login_sessions")
    login_time = models.DateTimeField(default=timezone.now)  # When the user logged in
    logout_time = models.DateTimeField(null=True, blank=True)  # When the user logged out
    login_duration = models.DurationField(default=timezone.timedelta())  # Duration of the session

    def __str__(self):
        return f"{self.user.username} - Session {self.loginsession_id}"


# New Models (Project, HouseType)
class HouseType(models.Model):
    housetype_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=20, choices=[('concrete', 'Concrete'), ('wooden', 'Wooden')])

    def __str__(self):
        return self.description


# Project Build
class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserHousewise, on_delete=models.CASCADE, related_name="projects")
    project_name = models.CharField(max_length=255, default="Unnamed Project")  # New field for project name
    length = models.DecimalField(max_digits=5, decimal_places=2)  # Meters with decimals
    width = models.DecimalField(max_digits=5, decimal_places=2)  # Meters with decimals
    height = models.DecimalField(max_digits=5, decimal_places=2)  # Meters with decimals
    cr_count = models.PositiveIntegerField(default=0)  # New field for CR count
    room_count = models.PositiveIntegerField(default=0)  # New field for room count
    date_time_created = models.DateTimeField(auto_now_add=True)  # Auto-generate date and time
    house_type = models.ForeignKey(HouseType, on_delete=models.CASCADE, related_name="projects")
    likes_count = models.PositiveIntegerField(default=0)  # Number of likes, default to 0
    is_published = models.BooleanField(default=False)  # Default is not published

    def __str__(self):
        return f"{self.project_name} (ID: {self.project_id}) for {self.user.username}"

    def update_counts(self):
        """Update the room and CR counts."""
        self.room_count = self.rooms.count()
        self.cr_count = self.crs.count()
        self.save()
        
class ProjectLike(models.Model):
    user = models.ForeignKey(UserHousewise, on_delete=models.CASCADE, related_name="liked_projects")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_likes")  # Change related_name
    liked_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')  # Prevent duplicate likes from the same user



#Feedbacks
class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    rating = models.PositiveIntegerField()  # For example, rating out of 5
    feedback_description = models.TextField()  # Paragraphs of feedback
    feedback_datetime = models.DateTimeField(auto_now_add=True)  # Automatically set the date and time
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="feedbacks", null=True, blank=True)

    def __str__(self):
        return f"Feedback {self.feedback_id} for Project {self.project.project_id if self.project else 'N/A'}"

#Comments sa admin sa feedback
class FeedbackComment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment_description = models.TextField()  # Paragraphs for the comment
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)

    def __str__(self):
        return f"Comment {self.comment_id} for Feedback {self.feedback.feedback_id if self.feedback else 'N/A'}"


#Roof Model
class Roof(models.Model):
    roof_id = models.AutoField(primary_key=True)
    roof_type = models.CharField(max_length=20, choices=[('colored_roof', 'Colored Roof'), ('plain_roof', 'Plain Roof')])
    trusses = models.CharField(
        max_length=20,
        choices=[('metal_trusses', 'Metal Trusses'), ('wooden_trusses', 'Wooden Trusses')],
        blank=True,  # Trusses will depend on roof_type choice
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="roofs")

    def save(self, *args, **kwargs):
        # Automatically set trusses based on roof_type
        if self.roof_type == 'colored_roof':
            self.trusses = 'metal_trusses'  # Automatically set for colored_roof
        super(Roof, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.roof_type} with {self.trusses}"

class Rooms(models.Model):
    ROOM_NUMBER_CHOICES = [
        ('1', '1'),
        ('2', '2'),
    ]

    ACTIVE_BUTTON_CHOICES = [
        ('TopStart', 'TopStart'),
        ('TopEnd', 'TopEnd'),
        ('BottomStart', 'BottomStart'),
        ('BottomEnd', 'BottomEnd'),
    ]

    room_id = models.AutoField(primary_key=True)
    room_number = models.CharField(
        max_length=1, 
        choices=ROOM_NUMBER_CHOICES, 
        default='1'
    )  # New field with options '1' or '2'
    room_length = models.DecimalField(max_digits=5, decimal_places=2)  # Meters with decimals
    room_width = models.DecimalField(max_digits=5, decimal_places=2)   # Meters with decimals
    active_button = models.CharField(
        max_length=20,
        choices=ACTIVE_BUTTON_CHOICES,
        default='TopStart'
    )  # New field for ActiveButton with options
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="rooms")

    def __str__(self):
        return f"Room {self.room_number}: {self.room_length}m x {self.room_width}m with ActiveButton at {self.active_button}"


#CR
class CR(models.Model):
    cr_id = models.AutoField(primary_key=True)
    cr_length = models.DecimalField(max_digits=5, decimal_places=2)  # Meters with decimals
    cr_width = models.DecimalField(max_digits=5, decimal_places=2)   # Meters with decimals
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="crs", null=True, blank=True)

    def __str__(self):
        return f"CR {self.cr_id} - {self.cr_length}m x {self.cr_width}m"

#Materials
class Materials(models.Model):
    materials_id = models.AutoField(primary_key=True)
    materials_name = models.CharField(max_length=100)  # Accepts letters and numbers
    project = models.ManyToManyField(Project, related_name="materials", blank=True)

    def __str__(self):
        return f"Material: {self.materials_name}"

#Price sa Materials
class MaterialPrice(models.Model):
    price_id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Accepts numbers with 2 decimal places
    date_time = models.DateTimeField(auto_now_add=True)  # Automatically set the date and time
    materials = models.ForeignKey(Materials, on_delete=models.CASCADE, related_name="prices")

    def __str__(self):
        return f"Price: {self.amount} for {self.materials.materials_name} at {self.date_time}"