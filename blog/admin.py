from django.contrib import admin

from blog.models import Blogpost


@admin.register(Blogpost)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'preview', 'created_at', 'publication')
    list_filter = ('publication',)
    search_filter = ('title', 'created_at',)

