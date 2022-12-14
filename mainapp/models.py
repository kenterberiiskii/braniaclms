from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

NULLABLE = {'blank': True, 'null': True}


class BaseModel(models.Model):
    created_at = models.DateField(auto_now_add=True, verbose_name='Создан')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    class Meta:
        abstract = True
        ordering = ('-created_at')

class NewsManager(models.Manager):

    def delete(self):
        pass

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

class News(BaseModel):
    # object = NewsManager()

    title = models.CharField(max_length=256, verbose_name='Заголовок')
    preamble = models.CharField(max_length=1024, verbose_name='Интро')

    body = models.TextField(verbose_name='Содержимое')
    body_as_markdown = models.BooleanField(default=False, verbose_name='Разметка в формате марк...')

    # created_at = models.DateField(auto_now_add=True, verbose_name='Создан')
    # update_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    # deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self) -> str:
        return f'#{self.pk} - {self.title}'

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()

class CoursesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

class Course(models.Model):
    objects = CoursesManager()
    title = models.CharField(max_length=256, verbose_name='заголовок')
    description = models.TextField(verbose_name='описание')

    cover = models.CharField(max_length=25, default="no_image.png", verbose_name="Cover")
    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Стоимость', default=0)

    created_at = models.DateField(auto_now_add=True, verbose_name='Создан')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self):
        return f'#{self.pk} - {self.title}'
    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    num = models.PositiveIntegerField(default=0, verbose_name='Номер урока')

    title = models.CharField(max_length=256, verbose_name='заголовок')
    description = models.TextField(verbose_name='описание')

    created_at = models.DateField(auto_now_add=True, verbose_name='Создан')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self):
        return f'{self.num}{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()

class CourseTeacher(models.Model):
    courses = models.ManyToManyField(Course)
    first_name = models.CharField(max_length=256, verbose_name='Имя')
    last_name = models.CharField(max_length=256, verbose_name='Фамилия')

    created_at = models.DateField(auto_now_add=True, verbose_name='Создан')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self):
        return f'{self.first_name}{self.last_name}'

    class Meta:
        verbose_name = 'курс к учителю'
        verbose_name_plural = 'курсы к учителям'

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()

class CourseFeedback(models.Model):

    RATING = ((5, "⭐⭐⭐⭐⭐"),
              (4, "⭐⭐⭐⭐"),
              (3, "⭐⭐⭐"),
              (2, "⭐⭐"),
              (1, "⭐")
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    feedback = models.TextField(default='Без отзыва', verbose_name='Отзыв')
    rating = models.SmallIntegerField(choices=RATING, default=5, verbose_name='Рейтинг')
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''

    def __str__(self):
        return f'отзыв на {self.course}  от {self.user}'