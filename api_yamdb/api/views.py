import uuid

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title, User

from api_yamdb.settings import DEFAULT_FROM_EMAIL

from .filters import TitlesFilter
from .mixins import ApiViewSet
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrAdminOrReadOnly
from .serializers import (AdminSerializer, CategorySerializer,
                          CommentSerializer, GenreSerializer,
                          GetTokenSerializer, ReviewSerializer,
                          SignUpSerializer, TitleGeneralSerializer,
                          TitleSlugSerializer, UserSerializer)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)

    def get_serializer_class(self):
        if (self.request.user.role in [User.ADMIN]
                or self.request.user.is_superuser):
            return AdminSerializer
        else:
            return UserSerializer

    def _read_only_defaults(self):
        if self.request.user.role in [User.USER]:
            read_only_fields = ('role',)
            return read_only_fields

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                user, data=request.data, partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class SignUp(APIView):
    """
    Регистрация по юзернейму и емейлу
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        User.objects.create(
            username=username,
            email=email
        )
        confirmation_code = uuid.uuid4()
        subject = 'Подтверждение регистрации'

        send_mail(
            subject=subject,
            message=(f'{subject} '
                     f'\nВаш confirmation_code: {confirmation_code}'),
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[email])
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetToken(APIView):
    """
    Получение токена в обмен на код доступа
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = get_object_or_404(
                User, username=serializer.validated_data.get('username')
            )
        except User.DoesNotExist:
            user = None

        confirmation_code = serializer.validated_data.get('confirmation_code')
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response(
                {'token': str(token)}, status=status.HTTP_200_OK
            )
        return Response('Неверный токен',
                        status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews_title.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        current_title = get_object_or_404(Title, pk=title_id)
        current_user = self.request.user
        serializer.save(title=current_title, author=current_user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get("review_id")
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
        )
        serializer.save(review=review, author=self.request.user)


class CategoriesViewSet(ApiViewSet):
    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(ApiViewSet):
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        Avg('reviews_title__score')
    ).order_by('id')
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return TitleSlugSerializer
        return TitleGeneralSerializer
