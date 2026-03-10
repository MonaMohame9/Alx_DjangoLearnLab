from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Post, Like
from notifications.models import Notification


class LikePostView(generics.GenericAPIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):

        post = generics.get_object_or_404(Post, pk=pk)

        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response({"message": "You already liked this post"})

        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            target=post
        )

        return Response({"message": "Post liked"})


class UnlikePostView(generics.GenericAPIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):

        post = generics.get_object_or_404(Post, pk=pk)

        Like.objects.filter(user=request.user, post=post).delete()

        return Response({"message": "Post unliked"})