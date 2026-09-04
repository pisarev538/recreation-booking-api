from django.contrib import admin
from .models import Article, Category, Comment, UserProfile, ArticleRating, ArticleView, Bookmark, Notification

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'create_at', 'update_at', 'is_published')
    list_filter = ('is_published', 'create_at')
    search_fields = ('title', 'content')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")
    search_fields = ("name",)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "article",
        "author_name",
        "author_email",
        "created_at",
        "is_approved"
    )
    list_filter = ("is_approved", "created_at")
    search_fields = ("author_name", "author_email", "content")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Настройка отображения профиля в админке"""
    list_display = (
        "user",
        "is_premium",
        "notifications_enabled",
        "article_count",
    )

    list_filter = (
        "is_premium",
        "user",
        "notifications_enabled"
    )

    search_fields = (
        "user__username",
        "phone_number",
        "location"
    )

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("user", "article", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "article__title", "notes")
 
 
@admin.register(ArticleRating)
class ArticleRatingAdmin(admin.ModelAdmin):
    list_display = ("user", "article", "rating", "rating_display", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("user__username", "article__title", "comment")
 
 
@admin.register(ArticleView)
class ArticleViewAdmin(admin.ModelAdmin):
    list_display = ("article", "user", "session_key", "viewed_at")
    list_filter = ("viewed_at",)
    search_fields = ("article__title", "user__username", "session_key")
 
 
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("recipient", "sender", "notification_type", "is_read", "created_at")
    list_filter = ("notification_type", "is_read", "created_at")
    search_fields = ("recipient__username", "sender__username", "message")
