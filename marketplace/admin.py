from django.contrib import admin
from .models import Category,Item,Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


