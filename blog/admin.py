from django.contrib import admin
from django.contrib.contenttypes import generic
from django.contrib.comments.models import Comment

from models import PostImage, Post, Series, Category

class PostImageInline(admin.StackedInline):
    """
    Post Image Admin Inline
    """
    model = PostImage
    extra = 0
    
class SeriesAdmin(admin.ModelAdmin):
    """
    Series Admin
    """
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)
    
class CommentInline(generic.GenericStackedInline):
    """
    Generic Comment Inline
    """
    model = Comment
    # specify the fk or the generic relation won't work properly
    ct_fk_field = 'object_pk'
    extra = 0
    
class PostAdmin(admin.ModelAdmin):
    """
    Blog Post Admin
    """
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'post_categories_string', 'is_published',
                    'publish_date', 'updated_on', 'tags', 'series',)
    search_fields = ('title', )
    list_filter = ('is_published', 'series', 'categories')
    list_editable=('is_published',)
    date_hierarchy = 'publish_date'
    fieldsets = (
        (None, { 'fields': ('title', 'slug',)}),
        ('Publishing', {'fields': ('publish_date', 'last_modified',
            'is_published', 'is_featured',)}),
        ('Catalog', {'fields': ('author', 'categories', 'series', 'tags',
            'meta_keywords',)}),
        (None, { 'fields': ('allow_comments',)}),
        ('Post', {'fields': ('summary', 'content',)}),
    )
    
    inlines = [PostImageInline,CommentInline,]
    
class CategoryAdmin(admin.ModelAdmin):
    """
    Category Admin
    """
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Series, SeriesAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
