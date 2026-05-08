from django.contrib import admin
from django.utils.html import format_html
from .models import Photo, Comment, Rating, Like


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display   = ['thumb', 'title', 'author', 'likes_count', 'comments_count', 'avg_rating_tag', 'location', 'created_at']
    list_display_links = ['title']
    list_filter    = ['created_at', 'author']
    search_fields  = ['title', 'caption', 'tags', 'location', 'author__username']
    ordering       = ['-created_at']
    list_per_page  = 20
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Photo Info', {'fields': ('author', 'title', 'image', 'caption')}),
        ('Details',   {'fields': ('location', 'people_present', 'tags')}),
        ('Timestamps',{'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def thumb(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:52px;height:52px;object-fit:cover;border-radius:8px;">',
                obj.image.url
            )
        return '—'
    thumb.short_description = ''

    def likes_count(self, obj):
        c = obj.likes.count()
        return format_html('<span style="color:#f472b6;font-weight:600;">♥ {}</span>', c)
    likes_count.short_description = 'Likes'

    def comments_count(self, obj):
        c = obj.comments.count()
        return format_html('<span style="color:#818cf8;">💬 {}</span>', c)
    comments_count.short_description = 'Comments'

    def avg_rating_tag(self, obj):
        r = obj.average_rating()
        if r:
            return format_html('<span style="color:#fbbf24;">★ {}</span>', r)
        return '—'
    avg_rating_tag.short_description = 'Rating'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display  = ['author', 'photo', 'short_text', 'created_at']
    list_filter   = ['created_at']
    search_fields = ['author__username', 'text', 'photo__title']
    ordering      = ['-created_at']
    list_per_page = 30
    readonly_fields = ['created_at']

    def short_text(self, obj):
        return obj.text[:70] + '…' if len(obj.text) > 70 else obj.text
    short_text.short_description = 'Comment'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display  = ['user', 'photo', 'score_stars', 'created_at']
    list_filter   = ['score', 'created_at']
    search_fields = ['user__username', 'photo__title']
    ordering      = ['-created_at']
    list_per_page = 30
    readonly_fields = ['created_at']

    def score_stars(self, obj):
        stars = '★' * obj.score + '☆' * (5 - obj.score)
        return format_html('<span style="color:#fbbf24;letter-spacing:3px;font-size:16px;">{}</span>', stars)
    score_stars.short_description = 'Score'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display  = ['user', 'photo', 'created_at']
    list_filter   = ['created_at']
    search_fields = ['user__username', 'photo__title']
    ordering      = ['-created_at']
    list_per_page = 30
    readonly_fields = ['created_at']
