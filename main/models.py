from django.db import models


class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)  # Код языка, например: en, ru
    name = models.CharField(max_length=50)  # Название языка, например: English, Russian

    def __str__(self):
        return self.name


class Category(models.Model):
    image = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.get_translation('en')

    def get_translation(self, language_code):
        translation = self.translations.filter(language__code=language_code).first()
        return translation.text if translation else "No translation available"


class PopularCourse(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.URLField(max_length=255, blank=True, null=True)
    lectures = models.IntegerField()
    quizzes = models.IntegerField()
    duration = models.CharField(max_length=50)
    students = models.IntegerField()
    price = models.CharField(max_length=50)

    def __str__(self):
        return self.get_translation('en')

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
    month = models.CharField(max_length=20, choices=MONTH_CHOICES)
    hour = models.CharField(max_length=50)
    image = models.JSONField()  # Stores an array of image URLs
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    total_slots = models.IntegerField()
    booked_slots = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    @property
    def available_slots(self):
        return self.total_slots - self.booked_slots

    def __str__(self):
        return self.get_translation('en')

    def get_translation(self, language_code):
        translation = self.translations.filter(language__code=language_code).first()
        return translation.title if translation else "No translation available"


class Review(models.Model):
    image = models.URLField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_translation(self, language_code):
        translation = self.translations.filter(language__code=language_code).first()
        return translation.comment if translation else "No translation available"


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


class ReviewTranslation(models.Model):
    review = models.ForeignKey(Review, related_name='translations', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    comment = models.TextField()

    class Meta:
        unique_together = ('review', 'language')

    def __str__(self):
        return f'{self.language.code}: {self.review.name}'
