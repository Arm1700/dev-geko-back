from django.core.exceptions import ValidationError
from django.db import models
import imghdr

STATUS_CHOICES = [
    ('yes', 'Yes'),
    ('no', 'No'),
]
STATUS_CHOICES_EVENT = [
    ('upcoming', 'Upcoming'),
    ('happening', 'Happening'),
    ('completed', 'Completed'),
]

MONTH_CHOICES = [
    ('January', 'January'),
    ('February', 'February'),
    ('March', 'March'),
    ('April', 'April'),
    ('May', 'May'),
    ('June', 'June'),
    ('July', 'July'),
    ('August', 'August'),
    ('September', 'September'),
    ('October', 'October'),
    ('November', 'November'),
    ('December', 'December'),
]


class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Category(models.Model):
    local_image = models.ImageField(upload_to='images/', blank=True, null=True)
    image_url = models.URLField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.get_translation('en') or "No translation available"

    def get_image(self):
        if self.local_image:
            return self.local_image.url
        elif self.image_url:
            return self.image_url
        return "No image available"

    def get_translation(self, language_code):
        translation = self.translations.filter(language__code=language_code).first()
        return translation.text if translation else "No translation available"


class PopularCourse(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    local_image = models.ImageField(upload_to='images/', blank=True, null=True)
    image_url = models.URLField(max_length=255, blank=True, null=True)
    duration = models.CharField(max_length=50)
    certification = models.TextField(default='yes', choices=STATUS_CHOICES)
    students = models.TextField(default='yes', choices=STATUS_CHOICES)
    studentGroup = models.TextField(default='yes', choices=STATUS_CHOICES)
    assessments = models.TextField(default='yes', choices=STATUS_CHOICES)
    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.get_translation('en')

    def get_image(self):
        if self.local_image:
            return self.local_image.url
        elif self.image_url:
            return self.image_url
        return None

    def get_translation(self, language_code):
        translation = self.translations.filter(language__code=language_code).first()
        return translation.title if translation else "No translation available"


class PopularCourseTranslation(models.Model):

    popular_course = models.ForeignKey(PopularCourse, related_name='translations', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    lang = models.CharField(max_length=50)
    desc = models.TextField()

    class Meta:
        unique_together = ('popular_course', 'language')

    def __str__(self):
        return f'{self.language.code}: {self.title}'


class Event(models.Model):
    day = models.IntegerField()
    hour = models.CharField(max_length=50)
    month = models.CharField(max_length=20, choices=MONTH_CHOICES)
    image = models.ImageField(upload_to='event_gallery_photos/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES_EVENT)
    # start_time = models.TimeField()
    # end_time = models.TimeField()
    # date = models.DateField()
    # def __str__(self):
    #     return f"Event on {self.date} from {self.start_time} to {self.end_time}"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)  # Ensure the base save is called
        images = form.cleaned_data.get('img', [])
        for image in images:
            EventGallery.objects.create(course=obj, img=image)

    def get_translation(self, language_code):
        translation = self.translations.filter(language__code=language_code).first()
        return translation.title if translation else "No translation available"


class EventGallery(models.Model):
    event = models.ForeignKey(Event, related_name='event_galleries', on_delete=models.CASCADE)
    img = models.ImageField(upload_to='event_gallery_photos/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        # Assuming you have a way to get the current language, set a default language if necessary
        current_language = 'en'  # Replace this with actual logic to get the current language
        # Fetch the translation for the event in the current language
        translation = self.event.translations.filter(language__code=current_language).first()
        if translation:
            return f"Event gallery {self.id} - {translation.title}"
        return f"Event gallery {self.id} - No title available"


class Review(models.Model):
    local_image = models.ImageField(upload_to='review_images/', blank=True, null=True)
    image_url = models.URLField(default='https://eduma.thimpress.com/wp-content/uploads/2022/07/thumnail-cate-7'
                                        '-170x170.png', max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    comment = models.TextField()

    def __str__(self):
        return self.name

    def get_image(self):
        if self.local_image:
            return self.local_image.url
        elif self.image_url:
            return self.image_url
        return None


class LessonInfo(models.Model):
    # Change ImageField to FileField for better flexibility with SVG files
    local_image = models.FileField(upload_to='lesson_images/', blank=True, null=True)

    image_url = models.URLField(
        default='https://eduma.thimpress.com/wp-content/uploads/2022/07/thumnail-cate-7-170x170.png',
        max_length=255, blank=True, null=True
    )

    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.get_translation("en")}'

    def get_translation(self, language_code):
        translation = self.translations.filter(language__code=language_code).first()
        return translation.title if translation else "No translation available"

    def clean(self):
        """
        Пользовательская валидация для проверки, что загруженный файл является SVG.
        """
        if self.local_image:
            # Проверка расширения файла на .svg
            if not self.local_image.name.endswith('.svg'):
                raise ValidationError('Можно загружать только файлы формата SVG.')

            # Проверка содержимого файла на валидный SVG
            try:
                self.local_image.seek(0)  # Сброс указателя в начало файла
                file_content = self.local_image.read(200)  # Читаем первые 200 байт файла
                # Проверка, что файл начинается с <?xml или содержит тег <svg>
                if not (file_content.startswith(b'<?xml') or b'<svg' in file_content.lower()):
                    raise ValidationError('Загруженный файл не является валидным SVG изображением.')
            except Exception as e:
                raise ValidationError(f"Ошибка при чтении файла: {str(e)}")

class CategoryTranslation(models.Model):
    category = models.ForeignKey(Category, related_name='translations', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    text = models.CharField(default='Default text', max_length=255)

    class Meta:
        unique_together = ('category', 'language')

    def __str__(self):
        return f'{self.language.code}: {self.text}'


class Team(models.Model):
    local_image = models.ImageField(upload_to='team_images/', blank=True, null=True)
    image_url = models.URLField(default='https://eduma.thimpress.com/wp-content/uploads/2022/07/thumnail-cate-7'
                                        '-170x170.png', max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.get_translation('en') or "No translation available"

    def get_image(self):
        if self.local_image:
            return self.local_image.url
        elif self.image_url:
            return self.image_url
        return "No image available"

    def get_translation(self, language_code):
        translation = self.translations.filter(language__code=language_code).first()
        return translation.name if translation else "No translation available"


class TeamTranslation(models.Model):
    team = models.ForeignKey(Team, related_name='translations', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    desc = models.TextField(default='Default desc')
    name = models.CharField(default='Default name', max_length=255)
    role = models.CharField(default='Default role', max_length=255)

    class Meta:
        unique_together = ('team', 'language')

    def __str__(self):
        return f'{self.language.code}: {self.name}'


class EventTranslation(models.Model):
    place = models.CharField(default='Default place', max_length=255)
    event = models.ForeignKey(Event, related_name='translations', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    title = models.CharField(default='Default title', max_length=255)
    description = models.CharField(default='Default description', max_length=255)

    class Meta:
        unique_together = ('event', 'language')

    def __str__(self):
        return f'{self.language.code}: {self.title}'


class LessonInfoTranslation(models.Model):
    lesson_info = models.ForeignKey(LessonInfo, related_name='translations', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    title = models.CharField(default='Default title', max_length=255)

    class Meta:
        unique_together = ('lesson_info', 'language')

    def __str__(self):
        return f'{self.language.code}: {self.title}'


class ContactMessage(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    country = models.CharField(max_length=255)
    whatsapp = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Message from {self.full_name} ({self.email})"
