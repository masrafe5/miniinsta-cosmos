from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Photo(models.Model):
    author         = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='photos'
    )
    title          = models.CharField(max_length=200)
    caption        = models.TextField(blank=True)
    image          = models.ImageField(upload_to='photos/%Y/%m/%d/')
    location       = models.CharField(max_length=200, blank=True)
    people_present = models.CharField(
        max_length=500,
        blank=True,
        help_text='Comma-separated names of people in the photo'
    )
    tags           = models.CharField(
        max_length=300,
        blank=True,
        help_text='Comma-separated tags, e.g. travel, food, nature'
    )
    created_at     = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['location']),
            models.Index(fields=['author']),
        ]

    def __str__(self):
        return f'{self.title} by {self.author.username}'

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(r.score for r in ratings) / ratings.count(), 1)
        return None

    def rating_count(self):
        return self.ratings.count()

    def get_tags_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]

    def get_people_list(self):
        return [p.strip() for p in self.people_present.split(',') if p.strip()]


class Comment(models.Model):
    photo      = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comments')
    author     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    text       = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        indexes = [models.Index(fields=['created_at'])]

    def __str__(self):
        return f'{self.author.username} on {self.photo.title}'


class Rating(models.Model):
    photo      = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='ratings')
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings')
    score      = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        unique_together = ('photo', 'user')
        indexes = [models.Index(fields=['photo', 'user'])]

    def __str__(self):
        return f'{self.user.username} rated {self.photo.title}: {self.score}/5'


class Like(models.Model):
    photo      = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='likes')
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        unique_together = ('photo', 'user')
        indexes = [models.Index(fields=['photo', 'user'])]

    def __str__(self):
        return f'{self.user.username} liked {self.photo.title}'


class SavedPhoto(models.Model):
    photo      = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='saved_entries')
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_photos')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        unique_together = ('photo', 'user')
        ordering = ['-created_at']
        indexes = [models.Index(fields=['user', 'photo'])]

    def __str__(self):
        return f'{self.user.username} saved {self.photo.title}'


class Notification(models.Model):
    user         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    actor        = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='actor_notifications'
    )
    verb         = models.CharField(max_length=120)
    target_photo = models.ForeignKey(Photo, null=True, blank=True, on_delete=models.CASCADE)
    read         = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['user', 'read'])]

    def __str__(self):
        return f'Notification for {self.user.username}: {self.verb}'
