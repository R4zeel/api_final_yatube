from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from .permissions import IsAuthorOrReadOnly, ReadOnly
from posts.models import Post, Group, Comment, Follow
from .serializers import (PostSerializer,
                          CommentSerializer,
                          GroupSerializer,
                          FollowSerializer
                          )


class CreateListViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """
    Вьюсет, поддерживающий действия 'create' и 'list'.
    """
    pass


class PostViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для операций с постами.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ('author', 'group',)
    ordering_fields = ('pub_date',)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def paginate_queryset(self, queryset):
        if 'limit' in self.request.GET or 'offset' in self.request.GET:
            return self.paginator.paginate_queryset(
                queryset,
                self.request,
                view=self
            )
        return None


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет для получения информации о группах.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AllowAny]


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для операций с комментариями.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return Comment.objects.all().filter(post=post.id)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post_id=post.id)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()


class FollowViewSet(CreateListViewSet):
    """
    Вьюсет для операций с подписками пользователей.
    """

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=following__username',)

    def get_queryset(self):
        following = Follow.objects.all().filter(user=self.request.user)
        return following

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
