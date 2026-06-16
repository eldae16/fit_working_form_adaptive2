from django.db import models

class Request(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    car = models.CharField(max_length=100, blank=True)
    service = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f"{self.name} - {self.phone}"

class Review(models.Model):
    name = models.CharField(max_length=100)
    car = models.CharField(max_length=100, blank=True)
    rating = models.PositiveSmallIntegerField(default=5)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f"{self.name} - {self.rating}★"
