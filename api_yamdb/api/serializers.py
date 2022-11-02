import datetime as dt

from rest_framework import serializers

from reviews.models import Category, Genre, Title  # isort:skip


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ("id",)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ("id",)
        model = Genre


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
        return 0

    def validate_year(self, value):
        year = dt.date.today().year
        if value >= year:
            raise serializers.ValidationError(
                "Год создания не может быть из будущего!"
            )
        return value
