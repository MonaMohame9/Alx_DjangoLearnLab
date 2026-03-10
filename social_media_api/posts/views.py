from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from .models import Post, Like
from notifications.models import Notification


class LikePostView(generics.GenericAPIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):

        post = get_object_or_404(Post, pk=pk)

        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )

        if not created:
            return Response(
                {"message": "You already liked this post"},
                status=status.HTTP_400_BAD_REQUEST
            )

        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            content_type=ContentType.objects.get_for_model(post),
            object_id=post.id
        )

        return Response({"message": "Post liked"})


class UnlikePostView(generics.GenericAPIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):

        post = get_object_or_404(Post, pk=pk)

        like = Like.objects.filter(
            user=request.user,
            post=post
        )

        if like.exists():
            like.delete()
            return Response({"message": "Post unliked"})

        return Response(
            {"error": "You have not liked this post"},
            status=status.HTTP_400_BAD_REQUEST
        )