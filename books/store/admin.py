from django.contrib import admin
from django.contrib.admin import ModelAdmin

from store.models import Book, UserBookRelation


@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_display = ['id', 'name', 'price', 'author_name', 'owner']


@admin.register(UserBookRelation)
class UserBookRelationAdmin(ModelAdmin):
    list_display = ['user', 'like', 'in_bookmarks', 'rate']
