from authentication.models import User, Profile
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


# User Serializer
# This serializer is responsible for serializing the User model.
# It includes fields id, username, and email. The password field is write-only for security.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Specifies the model to serialize.
        fields = ['id', 'username', 'email']  # Fields to include in the serialization.
        extra_kwargs = {
            'password': {'write_only': True}  # Makes the password field write-only.
        }


# Custom Token Serializer
# Extends TokenObtainPairSerializer to add additional information to the JWT token.
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Generate token using superclass method.
        token = super().get_token(user)

        # Custom claims added to the token.
        token['full_name'] = user.profile.full_name  # User's full name from the profile.
        token['username'] = user.username  # Username from the user model.
        token['email'] = user.email  # Email from the user's profile.
        token['bio'] = user.profile.bio  # Bio from the user's profile.
        token['image'] = str(user.profile.image)  # Image URL from the user's profile.
        token['verified'] = user.profile.verified  # Verification status from the user's profile.

        return token  # Return the customized token.


# Register Serializer
# This serializer is used for user registration. It includes email, username, and password fields.
# It also includes a password2 field for password confirmation.
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,
                                     validators=[validate_password])  # Password field with validation.
    password2 = serializers.CharField(write_only=True, required=True)  # Password confirmation field.

    class Meta:
        model = User  # Specifies the User model for serialization.
        fields = ['email', 'username', 'password', 'password2']  # Fields included in the serialization.

    def validate(self, attrs):
        # Custom validation method to check if passwords match.
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs  # Return attributes if validation passes.

    def create(self, validated_data):
        # Method to create a new user instance.
        user = User.objects.create(
            email=validated_data['email'],  # Set email from validated data.
            username=validated_data['username'],  # Set username from validated data.
        )

        user.set_password(validated_data['password'])
        user.save()

        return user