from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, authentication
from core.models import UserProfile
from core.serializers import UserProfileSerializer
from mongoengine.errors import DoesNotExist, ValidationError as MongoValidationError

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Allow safe methods (GET, HEAD, OPTIONS) for anyone.
    Allow modifying methods (POST, PUT, PATCH, DELETE, etc.) only for authenticated users.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

class UserProfileView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, username=None):
        if username:
            try:
                user = UserProfile.objects.get(username=username)
                serializer = UserProfileSerializer(user)
                return Response(serializer.data)
            except DoesNotExist:
                return Response({"detail": "UserProfile not found."}, status=status.HTTP_404_NOT_FOUND)
        # List all users if no username is provided
        users = UserProfile.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response(UserProfileSerializer(user).data, status=status.HTTP_201_CREATED)
            except MongoValidationError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, username=None):
        try:
            user = UserProfile.objects.get(username=username)
        except DoesNotExist:
            return Response({"detail": "UserProfile not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserProfileSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, username=None):
        try:
            user = UserProfile.objects.get(username=username)
        except DoesNotExist:
            return Response({"detail": "UserProfile not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserProfileSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username=None):
        try:
            user = UserProfile.objects.get(username=username)
        except DoesNotExist:
            return Response({"detail": "UserProfile not found."}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)