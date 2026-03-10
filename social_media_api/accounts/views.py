from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):

    try:
        user_to_follow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    if request.user == user_to_follow:
        return Response({"error": "You cannot follow yourself"}, status=400)

    request.user.following.add(user_to_follow)

    return Response({"message": f"You are now following {user_to_follow.username}"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):

    try:
        user_to_unfollow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    request.user.following.remove(user_to_unfollow)

    return Response({"message": f"You unfollowed {user_to_unfollow.username}"})