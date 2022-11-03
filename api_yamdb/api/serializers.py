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
        return round(obj.reviews.aggregate(Avg("score")).get("score__avg"), 1)

    def validate_year(self, value):
        year = dt.date.today().year
        if value >= year:
            raise serializers.ValidationError(
                "Год создания не может быть из будущего!"
            )
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )

    def validate(self, data):
        if data.get("username") == "me":
            raise serializers.ValidationError("Username указан неверно!")
        return data


class AuthSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username")


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=50)
