from rest_framework import serializers
from .models import Language, Category, Review, Event,  PopularCourse, CategoryTranslation, PopularCourseTranslation, ReviewTranslation

class ContactFormSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    message = serializers.CharField()


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('code', 'name')


class CategoryTranslationSerializer(serializers.ModelSerializer):
    language = LanguageSerializer()

    class Meta:
        model = CategoryTranslation
        fields = ('language', 'text')


class CategorySerializer(serializers.ModelSerializer):
    translations = CategoryTranslationSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'image', 'translations')

    # Метод для получения перевода на конкретный язык
    def to_representation(self, instance):
        language_code = self.context.get('language_code', None)  # Получаем код языка из контекста
        representation = super().to_representation(instance)

        if language_code:
            # Если указан язык, возвращаем только нужный перевод
            translation = next((t for t in representation['translations'] if t['language']['code'] == language_code),
                               None)
            representation['translation'] = translation
            representation.pop('translations')  # Удаляем все переводы, оставляем только один
        return representation


class PopularCourseTranslationSerializer(serializers.ModelSerializer):
    language = LanguageSerializer()

    class Meta:
        model = PopularCourseTranslation
        fields = ('language', 'lang' ,'title', 'skill_level',  'assessments', 'desc','certification')


class PopularCourseSerializer(serializers.ModelSerializer):
    translations = PopularCourseTranslationSerializer(many=True)
    category = CategorySerializer()  # Подключаем сериализатор для категорий

    class Meta:
        model = PopularCourse
        fields = ('id', 'category', 'image', 'lectures', 'quizzes', 'duration', 'students','price', 'translations')

    # Метод для возвращения перевода на нужном языке
    def to_representation(self, instance):
        language_code = self.context.get('language_code', None)  # Получаем код языка из контекста
        representation = super().to_representation(instance)

        if language_code:
            # Если указан язык, возвращаем только нужный перевод
            translation = next((t for t in representation['translations'] if t['language']['code'] == language_code),
                               None)
            representation['translation'] = translation
            representation.pop('translations')  # Удаляем все переводы, оставляем только один
        return representation


class EventSerializer(serializers.ModelSerializer):
    available_slots = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = '__all__'

class ReviewTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewTranslation
        fields = ['language', 'comment']

class ReviewSerializer(serializers.ModelSerializer):
    translations = ReviewTranslationSerializer(many=True)

    class Meta:
        model = Review
        fields = ['id', 'image', 'name', 'translations']