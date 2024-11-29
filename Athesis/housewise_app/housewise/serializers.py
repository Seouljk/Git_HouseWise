from rest_framework import serializers
from .models import UserHousewise, UserType

class UserHousewiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserHousewise
        fields = ['name', 'email', 'username', 'age', 'password']
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
            age=validated_data['age'],
            user_type=user_type
        )
        return user
