from django.db import models


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
        return self.get_translation('en')

    def get_image(self):
        if self.local_image:
            return self.local_image.url
        elif self.image_url:
            return self.image_url
        return None

    def get_translation(self, language_code):
        translation = self.translations.filter(language__code=language_code).first()
        return translation.text if translation else "No translation available"


class PopularCourse(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    local_image = models.ImageField(upload_to='images/', blank=True, null=True)
    image_url = models.URLField(max_length=255, blank=True, null=True)
    lectures = models.IntegerField()
    quizzes = models.IntegerField()
    duration = models.CharField(max_length=50)
    students = models.IntegerField()
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


class Event(models.Model):
    STATUS_CHOICES = [
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
    day = models.IntegerField()
    hour = models.CharField(max_length=50)
    month = models.CharField(max_length=20, choices=MONTH_CHOICES)
    image = models.ImageField(upload_to='event_gallery_photos/', blank=True, null=True)
    total_slots = models.IntegerField()
    booked_slots = models.IntegerField()
    order = models.PositiveIntegerField(default=0, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    @property
    def available_slots(self):
        return self.total_slots - self.booked_slots

    def __str__(self):
        return self.get_translation('en')

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
    image_url = models.URLField(max_length=255, blank=True, null=True)
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
    icon = models.CharField(max_length=50)
    count = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.get_translation("en")}: {self.count}'

    def get_translation(self, language_code):
        translation = self.translations.filter(language__code=language_code).first()
        return translation.title if translation else "No translation available"


class CategoryTranslation(models.Model):
    category = models.ForeignKey(Category, related_name='translations', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    class Meta:
        unique_together = ('category', 'language')

    def __str__(self):
        return f'{self.language.code}: {self.text}'


class PopularCourseTranslation(models.Model):
    popular_course = models.ForeignKey(PopularCourse, related_name='translations', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    skill_level = models.CharField(max_length=50)
    assessments = models.CharField(max_length=50)
    lang = models.CharField(max_length=50)
    desc = models.TextField()
    certification = models.TextField()

    class Meta:
        unique_together = ('popular_course', 'language')

    def __str__(self):
        return f'{self.language.code}: {self.title}'


class EventTranslation(models.Model):
    place = models.CharField(max_length=255)
    event = models.ForeignKey(Event, related_name='translations', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        unique_together = ('event', 'language')

    def __str__(self):
        return f'{self.language.code}: {self.title}'


class LessonInfoTranslation(models.Model):
    lesson_info = models.ForeignKey(LessonInfo, related_name='translations', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    class Meta:
        unique_together = ('lesson_info', 'language')

    def __str__(self):
        return f'{self.language.code}: {self.title}'
