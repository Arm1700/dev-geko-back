from django.contrib import admin
from django import forms
from .models import Event, EventTranslation, Category, CategoryTranslation, PopularCourse, PopularCourseTranslation, \
    Review, ReviewTranslation, Language, LessonInfoTranslation, LessonInfo
from .filters import ReviewLanguageFilter


# Общий класс для переключения языков
class LanguageSwitcherMixin:
    @staticmethod
    def get_language_switcher_form(request, session_key, default_language='en'):
        languages = Language.objects.all()
        current_language = request.session.get(session_key, default_language)

        class LanguageForm(forms.Form):
            language = forms.ChoiceField(choices=[(lang.code, lang.name) for lang in languages])

        if request.method == 'POST':
            language_form = LanguageForm(request.POST)
            if language_form.is_valid():
                current_language = language_form.cleaned_data['language']
                request.session[session_key] = current_language
        else:
            language_form = LanguageForm(initial={'language': current_language})

        return language_form, current_language

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        language_form, current_language = self.get_language_switcher_form(request, session_key=self.session_key)
        extra_context = extra_context or {}
        extra_context['language_form'] = language_form

        return super().changeform_view(request, object_id, form_url, extra_context)


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


admin.site.register(Language, LanguageAdmin)


class PopularCourseTranslationInline(admin.StackedInline):
    model = PopularCourseTranslation
    extra = 1
    fields = (
        'language',
        'title',
        'skill_level',
        'assessments',
        'desc',
        'certification',
    )


class PopularCourseAdmin(LanguageSwitcherMixin, admin.ModelAdmin):
    inlines = [PopularCourseTranslationInline]
    list_display = ('id', 'category', 'lectures', 'quizzes', 'duration', 'students', 'price')
    search_fields = ('translations__title', 'category__translations__text')
    list_filter = ('category', 'students', 'translations__skill_level')
    session_key = 'popular_course_translation_language'


admin.site.register(PopularCourse, PopularCourseAdmin)


class CategoryTranslationInline(admin.TabularInline):
    model = CategoryTranslation
    extra = 1


class CategoryAdmin(LanguageSwitcherMixin, admin.ModelAdmin):
    inlines = [CategoryTranslationInline]
    list_display = ('id', 'image')
    search_fields = ('translations__text', 'image')
    list_filter = ('translations__language',)
    session_key = 'category_translation_language'


admin.site.register(Category, CategoryAdmin)


class LessonInfoTranslationInline(admin.StackedInline):
    model = LessonInfoTranslation
    extra = 1
    fields = (
        'language',
        'title',
    )


class LessonInfoAdmin(LanguageSwitcherMixin, admin.ModelAdmin):
    inlines = [LessonInfoTranslationInline]
    list_display = ('id', 'icon', 'count')
    search_fields = ('translations__title',)
    list_filter = ('icon',)
    session_key = 'lesson_info_translation_language'


admin.site.register(LessonInfo, LessonInfoAdmin)


class EventTranslationInline(admin.StackedInline):
    model = EventTranslation
    extra = 1
    fields = (
        'language',
        'title',
        'description',
        'place'
    )


class EventAdmin(LanguageSwitcherMixin, admin.ModelAdmin):
    inlines = [EventTranslationInline]
    list_display = ('id', 'day', 'month', 'hour', 'status', 'total_slots', 'booked_slots', 'cost')
    search_fields = ('translations__title',)
    list_filter = ('month', 'status')
    session_key = 'event_translation_language'


admin.site.register(Event, EventAdmin)


class ReviewTranslationInline(admin.StackedInline):
    model = ReviewTranslation
    extra = 1
    fields = ('language', 'comment')


class ReviewAdmin(LanguageSwitcherMixin, admin.ModelAdmin):
    inlines = [ReviewTranslationInline]
    list_display = ('id', 'name')
    search_fields = ('translations__comment', 'name')
    list_filter = (ReviewLanguageFilter,)
    session_key = 'review_translation_language'


admin.site.register(Review, ReviewAdmin)
