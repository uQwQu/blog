from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from apps.profiles.models import Profile
from apps.profiles.serializers import (
    AvatarUploadSerializer,
    ProfileSerializer,
    UpdateProfileSerializer,
)

from .tasks import upload_avatar_to_cloudinary

User = get_user_model()


class ProfileListAPIView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Profile.objects.filter(private=False)


class MyProfileDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer

    def get_object(self) -> Profile:
        return get_object_or_404(Profile, user=self.request.user)


class ProfileDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        username = self.kwargs.get("username")
        profile = get_object_or_404(Profile, user__username=username)
        if profile.user == self.request.user:
            return profile
        if not profile.private:
            return profile
        raise PermissionDenied()


class ProfileUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UpdateProfileSerializer

    def get_object(self) -> Profile:
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def perform_update(self, serializer) -> Profile:
        user_data = serializer.validated_data.pop("user", {})
        username = user_data.get("username")
        if username and User.objects.filter(username=username).exclude(id=self.request.user.id).exists():
            raise PermissionDenied("This username is already taken!")
        profile = serializer.save()
        User.objects.filter(id=self.request.user.id).update(**user_data)
        return profile


@api_view(["PATCH"])
def avatar_upload_api_view(request):
    profile = request.user.profile
    serializer = AvatarUploadSerializer(profile, data=request.data)

    if serializer.is_valid():
        image = serializer.validated_data["avatar"]

        image_content = image.read()

        upload_avatar_to_cloudinary.delay(str(profile.id), image_content)

        return Response(
            {"message": "Avatar upload started..."}, status=status.HTTP_202_ACCEPTED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
