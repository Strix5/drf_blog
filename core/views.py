from django.shortcuts import render
from django.core.mail import send_mail
from rest_framework import filters
from rest_framework import viewsets, permissions, pagination, generics, views
from rest_framework.response import Response

from .models import Post, Comment
from .serializers import PostModelSerializer, ContactSerializer, RegistrationSerializer, UserSerializer, \
    CommentSerializer


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'


class PostViewSet(viewsets.ModelViewSet):
    search_fields = ['content', 'h1']
    filter_backends = (filters.SearchFilter,)
    serializer_class = PostModelSerializer
    queryset = Post.objects.order_by('-created')
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberSetPagination

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     for t in queryset.distinct('created'):
    #         queryset['id'].created = t.split('.')
    #     return queryset


class AsideAPIView(generics.ListAPIView):
    queryset = Post.objects.order_by('-created')[:5]
    serializer_class = PostModelSerializer
    permission_classes = [permissions.AllowAny]


class FeedBackAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer_class = ContactSerializer(data=request.data)
        if serializer_class.is_valid():
            data = serializer_class.validated_data
            name = data.get('name')
            from_email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
            send_mail(f'От {name} | {subject}', message, from_email, ['topsonsven@gmail.com'])
            return Response({"success": "Sent"})


class RegistrationAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'message': 'Пользователь успешно создан',
        })


class ProfileAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return Response({
            'user': UserSerializer(request.user, context=self.get_serializer_context()).data
        })


class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_slug = self.kwargs['post_slug'].lower()
        post = Post.objects.get(slug=post_slug)
        return Comment.objects.filter(post=post)


class CommentDestroy(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(pk=self.kwargs['pk'], username=self.request.user)
