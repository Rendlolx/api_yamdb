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


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

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
