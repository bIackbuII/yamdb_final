from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (ReviewViewSet,
                    SignUp,
                    GetToken,
                    UserViewSet,
                    GenreViewSet,
                    TitleViewSet,
                    CommentViewSet,
                    CategoriesViewSet)

app_name = 'api'

r_v1 = DefaultRouter()

r_v1.register('users', UserViewSet)
r_v1.register('categories', CategoriesViewSet)
r_v1.register('genres', GenreViewSet)
r_v1.register('titles', TitleViewSet)
r_v1.register('comments', CommentViewSet, basename='reviews')
r_v1.register(r'titles/(?P<title_id>\d+)/reviews',
              ReviewViewSet, basename='reviews')
r_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
              CommentViewSet, basename='reviews')

urlpatterns = [
    path('v1/auth/signup/', SignUp.as_view(), name='sign_up'),
    path('v1/auth/token/', GetToken.as_view(), name='get_token'),
    path('v1/', include(r_v1.urls)),
]
