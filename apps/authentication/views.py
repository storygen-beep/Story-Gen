"""
Authentication views with FastAPI compatibility.
"""

from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .models import User, UserStatus
from .serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    RefreshTokenSerializer,
    RegisterSerializer,
    TokenResponseSerializer,
    UserSerializer,
)


class RegisterView(APIView):
    """Register new user - matches FastAPI endpoint exactly."""

    permission_classes = [AllowAny]

    @extend_schema(
        summary="Register new user",
        description="Create a new user account and return access tokens.",
        request=RegisterSerializer,
        responses={201: TokenResponseSerializer},
        tags=["Authentication"],
    )
    def post(self, request):
        """Handle user registration."""
        # Handle registration without password2 confirmation
        data = request.data.copy()

        # Validate password manually since frontend doesn't send password2
        password = data.get("password", "")
        if len(password) < 8:
            return Response(
                {"detail": "Password must be at least 8 characters long"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = RegisterSerializer(data=data)

        if serializer.is_valid():
            # Create user
            user = serializer.save()

            # Update last login
            user.update_last_login()

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Return response matching FastAPI format exactly
            response_data = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer",
                "expires_in": 86400,  # 1 day in seconds
                "user": UserSerializer(user).data,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        # Return validation errors in format frontend expects
        errors = serializer.errors
        if "email" in errors:
            return Response(
                {"detail": errors["email"][0]}, status=status.HTTP_400_BAD_REQUEST
            )
        if "username" in errors:
            return Response(
                {"detail": errors["username"][0]}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"detail": "Registration failed"}, status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    """Login user - matches FastAPI endpoint exactly."""

    permission_classes = [AllowAny]

    @extend_schema(
        summary="Login user",
        description="Authenticate user and return access tokens.",
        request=LoginSerializer,
        responses={200: TokenResponseSerializer},
        tags=["Authentication"],
    )
    def post(self, request):
        """Handle user login."""
        serializer = LoginSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            # Update last login
            user.update_last_login()

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Return response matching FastAPI format exactly
            response_data = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer",
                "expires_in": 86400,  # 1 day in seconds
                "user": UserSerializer(user).data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        # Return error in format frontend expects
        return Response(
            {"detail": "Incorrect email or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class RefreshTokenView(APIView):
    """Refresh token - matches FastAPI endpoint exactly."""

    permission_classes = [AllowAny]

    @extend_schema(
        summary="Refresh token",
        description="Refresh access token using refresh token.",
        request=RefreshTokenSerializer,
        responses={200: TokenResponseSerializer},
        tags=["Authentication"],
    )
    def post(self, request):
        """Handle token refresh."""
        serializer = RefreshTokenSerializer(data=request.data)

        if serializer.is_valid():
            try:
                refresh = RefreshToken(serializer.validated_data["refresh_token"])

                # Get user from token
                user_id = refresh["sub"]  # Use 'sub' claim like FastAPI
                user = User.objects.get(id=user_id)

                if not user.is_active or user.status != UserStatus.ACTIVE:
                    return Response(
                        {"detail": "User not found or inactive"},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )

                # Generate new token pair
                new_refresh = RefreshToken.for_user(user)
                access_token = str(new_refresh.access_token)
                refresh_token = str(new_refresh)

                # Return response matching FastAPI format
                response_data = {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_type": "Bearer",
                    "expires_in": 86400,  # 1 day in seconds
                    "user": UserSerializer(user).data,
                }

                return Response(response_data, status=status.HTTP_200_OK)

            except (InvalidToken, TokenError, User.DoesNotExist):
                return Response(
                    {"detail": "Invalid refresh token"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        return Response(
            {"detail": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED
        )


class VerifyTokenView(APIView):
    """Verify token - custom endpoint for frontend compatibility."""

    permission_classes = [AllowAny]

    @extend_schema(
        summary="Verify token",
        description="Verify if access token is valid - for frontend compatibility.",
        tags=["Authentication"],
    )
    def post(self, request):
        """Handle token verification."""
        # The JWT authentication middleware will handle token validation
        # If we reach here with a valid token, return success
        auth_header = request.META.get("HTTP_AUTHORIZATION")

        if not auth_header or not auth_header.startswith("Bearer "):
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Extract token and validate
        token = auth_header.split(" ")[1]

        try:
            # This will raise an exception if token is invalid
            AccessToken(token)

            return Response({"valid": True}, status=status.HTTP_200_OK)
        except (InvalidToken, TokenError):
            return Response(
                {"detail": "Token is invalid or expired"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class MeView(APIView):
    """Get current user - matches FastAPI /me endpoint exactly."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get current user",
        description="Get current authenticated user's profile information.",
        responses={200: UserSerializer},
        tags=["Authentication"],
    )
    def get(self, request):
        """Handle getting current user."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    """Change password endpoint."""

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        """Return the current user."""
        return self.request.user

    @extend_schema(
        summary="Change password",
        description="Change the current user's password.",
        tags=["Authentication"],
    )
    def update(self, request, *args, **kwargs):
        """Update user password."""
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Set the new password
            self.object.set_password(serializer.validated_data["new_password"])
            self.object.save()

            return Response(
                {"message": "Password updated successfully"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
