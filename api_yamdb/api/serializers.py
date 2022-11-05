import datetime as dt

from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Category, Genre, Title, User  # isort:skip


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ("id",)
        model = Category
        lookup_field = "slug"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ("id",)
        model = Genre
        lookup_field = "slug"


class GenreSlug(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = GenreSerializer(value)
        return serializer.data


class CategorySlug(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = CategorySerializer(value)
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSlug(
        many=True,
        slug_field="slug",
        queryset=Genre.objects.all(),
    )
    category = CategorySlug(
        slug_field="slug",
        queryset=Category.objects.all(),
    )

    class Meta:
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )
        model = Title

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg("score")).get("score__avg")

    def validate_year(self, value):
        year = dt.date.today().year
        if value >= year:
            raise serializers.ValidationError(
                "Год создания не может быть из будущего!"
            )
        return value


class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        email = serializers.EmailField(required=True)
        username = serializers.CharField(required=True)
        
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )

    def validate_username(self, value):
        """Проверяем, что нельзя создать пользователя с username = "me"
        и, что нельзя создать с одинаковым username."""
        username = value.lower()
        if username == 'me':
            raise serializers.ValidationError(
                'Пользователя с username="me" создавать нельзя.'
            )
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                f'Пользователь с таким username — {username} — уже существует.'
            )
        return value

    def validate_email(self, value):
        """Проверяем, что нельзя создать пользователя с одинаковым email."""
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                f'Пользователь с таким Email — {email} — уже существует.'
            )
        return value



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username")


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=50)
