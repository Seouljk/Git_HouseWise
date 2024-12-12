from rest_framework import serializers
from .models import UserHousewise, UserType
from .models import Project, CR, Rooms, Roof, ProjectLike, HouseType, Feedback

class UserHousewiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserHousewise
        fields = ['name', 'email', 'username', 'birthdate', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Fetch the 'user' UserType instance (usertype_id = 2)
        user_type = UserType.objects.get(usertype_id=2)
        
        # Create a new user using the manager
        user = UserHousewise.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            birthdate=validated_data['birthdate'],  # Save birthdate
            user_type=user_type
        )
        return user

class FeedbackSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.project_name', read_only=True)  # Include project name
    project_id = serializers.IntegerField(source='project.project_id', read_only=True)  # Include project ID

    class Meta:
        model = Feedback
        fields = [
            'feedback_id',
            'rating',
            'feedback_description',
            'feedback_datetime',
            'project_id',  # ID of the associated project
            'project_name',  # Name of the associated project
        ]


class RoofSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roof
        fields = ['roof_type', 'trusses']

class CRSerializer(serializers.ModelSerializer):
    class Meta:
        model = CR
        fields = ['cr_length', 'cr_width']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = ['room_number', 'room_length', 'room_width', 'active_button']

class HouseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseType
        fields = ['description']

class ProjectSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)  # Add this line
    crs = CRSerializer(many=True, read_only=True)
    rooms = RoomSerializer(many=True, read_only=True)
    roofs = RoofSerializer(many=True, read_only=True)  # Include Roof data
    housetype = serializers.CharField(source='house_type.description', read_only=True)  # Directly fetch the description
    liked = serializers.SerializerMethodField()  # Add liked field
    likes = serializers.IntegerField(source="likes_count", read_only=True)  # Map likes_count to likes

    def get_liked(self, obj):
        user = self.context.get('request').user  # Access the user from the request context
        if user.is_authenticated:
            return ProjectLike.objects.filter(user=user, project=obj).exists()
        return False

    class Meta:
        model = Project
        fields = [
            'project_id',
            'project_name',
            'length',
            'width',
            'height',
            'cr_count',
            'room_count',
            'is_published',
            'user_username',
            'crs',
            'rooms',
            'roofs',
            'likes',  # Use likes instead of likes_count in the API response
            'liked',  # Include liked status for the current user
            'housetype',
        ]