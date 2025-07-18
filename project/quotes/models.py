from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now


class SourceType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Source(models.Model):
    name = models.CharField(max_length=200)
    type = models.ForeignKey(SourceType, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.name} ({self.type.name if self.type else 'Без типа'})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Источник'
        verbose_name_plural = 'Источники'


class Quote(models.Model):
    text = models.TextField(unique=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, blank=True)
    weight = models.PositiveIntegerField(default=1)
    likes = models.ManyToManyField(User, related_name='liked_quotes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_quotes', blank=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.source and Quote.objects.filter(source=self.source).count() >= 3 and not self.pk:
            raise ValidationError(f"У источника {self.source} уже есть 3 цитаты")
        if self.weight <= 0:
            raise ValidationError("Вес цитаты должен быть положительным числом")

    def __str__(self):
        source_name = self.source.name if self.source else "Без источника"
        return f"{self.text[:50]}... ({source_name})"

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def dislikes_count(self):
        return self.dislikes.count()

    @property
    def popularity(self):
        return self.likes_count - self.dislikes_count

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Цитата'
        verbose_name_plural = 'Цитаты'
