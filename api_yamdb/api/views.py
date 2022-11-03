import django_filters
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import (
    CharFilter,
    DjangoFilterBackend,
    FilterSet,
)
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import (
    IsAuthorModeratorPermission,
    IsStaffAdminPermission,
    IsUserSelfPermission,
)
from .utils import generate_and_send_confirmation_code_to_email

from .permissions import IsAdminOrReadOnly  # isort:skip

from .serializers import (  # isort:skip
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    UserSerializer,
    AuthSignUpSerializer,
    AuthTokenSerializer,
)
from reviews.models import Category, Genre, Title, User  # isort:skip


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name="category", lookup_expr="slug"
    )
    genre = django_filters.CharFilter(field_name="genre", lookup_expr="slug")
    name = django_filters.CharFilter(
        field_name="name", lookup_expr="icontains"
    )

    class Meta:
        model = Title
        fields = ["category", "genre", "name", "year"]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsStaffAdminPermission,)
    search_fields = ("=username",)
    lookup_field = "username"

    @action(
        detail=False,
        methods=["GET", "PATCH"],
        permission_classes=(IsUserSelfPermission,),
    )
    def me(self, request):
        if request.method == "PATCH":
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def signup_new_user(request):
    username = request.data.get("username")
    if not User.objects.filter(username=username).exists():
        serializer = AuthSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data["username"] != "me":
            serializer.save()
            generate_and_send_confirmation_code_to_email(username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            "Username указан невено!", status=status.HTTP_400_BAD_REQUEST
        )
    user = get_object_or_404(User, username=username)
    serializer = AuthSignUpSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    if serializer.validated_data["email"] == user.email:
        serializer.save()
        generate_and_send_confirmation_code_to_email(username)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(
        "Почта указана неверно!", status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["POST"])
def get_token(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data["username"]
    confirmation_code = serializer.validated_data["confirmation_code"]
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(
            "Пользователь не найден", status=status.HTTP_404_NOT_FOUND
        )
    if user.confirmation_code == confirmation_code:
        refresh = RefreshToken.for_user(user)
        token_data = {"token": str(refresh.access_token)}
        return Response(token_data, status=status.HTTP_200_OK)
    return Response(
        "Код подтверждения неверный", status=status.HTTP_400_BAD_REQUEST
    )
