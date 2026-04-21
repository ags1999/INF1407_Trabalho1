from django.db import models
from django.contrib.auth.models import User

class Livro(models.Model):
    google_volume_id =models.CharField(max_length=255, default='')
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    cover_url = models.URLField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'google_volume_id'], name='unique_user_book')
        ]

    def __str__(self):
        return self.title