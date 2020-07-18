from django.db import models
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags import humanize
from django.utils import timezone, text
from django.urls import reverse
import itertools


# Create your models here.
class Note(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique_for_date='publish')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse(
            'notes:note_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )
    
    def get_delete_url(self):
        return reverse(
            'notes:note_delete',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )
    
    def get_update_url(self):
        return reverse(
            'notes:note_update',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )
    
    def get_date(self):
        return humanize.naturaltime(self.publish)
    
    def _generate_slug(self):
        value = self.title
        slug_candidate = slug_original = text.slugify(value)
        for i in itertools.count(1):
            if not Note.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = f"{slug_original}-{i}"
        self.slug = slug_candidate
    
    def save(self, *args, **kwargs):
        if self.id is None:
            self._generate_slug()
        super().save(*args, **kwargs)