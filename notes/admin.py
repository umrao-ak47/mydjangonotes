from django.contrib import admin
from .models import Note

# Register your models here.
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish',)
    list_filter = ('created', 'publish', 'author',)
    search_fields = ('title', 'body',)
    raw_id_fields = ('author',)
    prepopulated_fields = {'slug':('title',)}
    date_hierarchy = 'publish'
    ordering = ('publish', )