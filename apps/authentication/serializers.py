"""
Authentication serializers with FastAPI compatibility.
"""

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, UserStatus


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model that matches FastAPI response format."""

    id = serializers.UUIDField(read_only=True)
    display_name = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(source="date_joined", read_only=True)
    last_login_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "full_name",
            "avatar_url",
            "role",
            "status",
            "is_verified",
            "display_name",
            "created_at",
            "last_login_at",
        )
        read_only_fields = ("id", "created_at", "last_login_at", "display_name")

    def get_display_name(self, obj):
        """Get display name for user."""
        return obj.full_name or obj.username or obj.email.split("@")[0]

    def to_representation(self, instance):
        """Convert to dict matching FastAPI format."""
        data = super().to_representation(instance)
        # Convert UUID to string for JSON compatibility
        data["id"] = str(instance.id)
        # Convert datetime to ISO format strings
        if data["created_at"]:
            data["created_at"] = instance.date_joined.isoformat()
        if data["last_login_at"]:
            data["last_login_at"] = instance.last_login_at.isoformat()
        return data


class RegisterSerializer(serializers.Serializer):
    """Serializer for user registration matching FastAPI format."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    full_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    username = serializers.CharField(max_length=50, required=False, allow_blank=True)

    def validate_email(self, value):
        """Validate email is unique."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value

    def validate_username(self, value):
        """Validate username is unique if provided."""
        if value and User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken")
        return value or None

    def create(self, validated_data):
        """Create new user."""
        password = validated_data.pop("password")
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data.get("username") or None,
            full_name=validated_data.get("full_name") or None,
            password=password,
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login matching FastAPI format."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        """Validate user credentials."""
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"),
                username=email,  # Our User model uses email as USERNAME_FIELD
                password=password,
            )

            if not user:
                raise serializers.ValidationError("Incorrect email or password")

            if not user.is_active:
                raise serializers.ValidationError("User account is disabled")

            if user.status != UserStatus.ACTIVE:
                raise serializers.ValidationError("User account is not active")

            attrs["user"] = user
            return attrs
        else:
            raise serializers.ValidationError("Must include email and password")


class TokenResponseSerializer(serializers.Serializer):
    """Serializer for token response matching FastAPI format exactly."""

    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    token_type = serializers.CharField(default="Bearer")
    expires_in = serializers.IntegerField(default=86400)  # 1 day in seconds
    user = UserSerializer()


class RefreshTokenSerializer(serializers.Serializer):
    """Serializer for token refresh matching FastAPI format."""

    refresh_token = serializers.CharField(required=True)

    def validate_refresh_token(self, value):
        """Validate and decode refresh token."""
        try:
            token = RefreshToken(value)
            # Validate token is not blacklisted and is still valid
            token.check_blacklist()
        except Exception:
            raise serializers.ValidationError("Invalid or expired refresh token")

        return value


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password."""

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        """Validate old password."""
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value
