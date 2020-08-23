from django.contrib import admin
from .models import *


@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = ('id','external_id','name')



@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id','name')

@admin.register(Subgenre)
class SubGenreAdmin(admin.ModelAdmin):
    list_display = ('id','name')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id','name','author')