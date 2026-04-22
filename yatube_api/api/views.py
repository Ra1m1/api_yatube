from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from posts.models import Post, Group
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('Чооо это ж не твое >.<')
        super().perform_update(serializer)

    def perform_destroy(self, post_to_delete):
        if post_to_delete.author != self.request.user:
            raise PermissionDenied('Так эт не твоё, нельзя удалять бож')
        post_to_delete.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('Нельзя!!!!')
        super().perform_update(serializer)

    def perform_destroy(self, opa):
        if opa.author != self.request.user:
            raise PermissionDenied('Нееееееет')
        opa.delete()
