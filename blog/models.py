from datetime import datetime

from django.db import models
from django.contrib.comments.models import Comment
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.sitemaps import ping_google
from django.contrib.comments.moderation import CommentModerator, moderator
from django.db.models import permalink

from tagging.models import Tag, TaggedItem
from tagging.fields import TagField

import settings

from managers import PostManager, PublishedPostManager, PostImageManager

class Series(models.Model):
    """
    Series of Posts
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    summary = models.TextField(blank=True)
    preface = models.TextField(blank=True)
    created_on = models.DateTimeField(default=datetime.now)
    
    @models.permalink
    def get_absolute_url(self):
        return ('blog.views.series_detail', [self.slug,])

    class Meta:
        ordering = ('-created_on',)
        verbose_name_plural = 'series'
        
    def __unicode__(self):
        return self.title


class Category(models.Model):
    """
    Category
    """
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    summary = models.TextField(blank=True)

    @models.permalink
    def get_absolute_url(self):
        return ('blog.views.category_detail', [self.slug,])
    
    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'categories'
    
    def __unicode__(self):
        return self.title

    
class Post(models.Model):
    """
    Post
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique_for_date='publish_date')
    author = models.ForeignKey(User)
    publish_date = models.DateTimeField(default=datetime.now)
    last_modified = models.DateTimeField(default=datetime.now)
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False,)
    allow_comments = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, blank=True,
        related_name='posts')
    series = models.ForeignKey(Series, blank=True, null=True,
        related_name='posts')
    tags = TagField()
    meta_keywords = models.CharField(max_length=255, blank=True)
    summary = models.TextField(
        help_text='Also doubles as the meta description')
    content = models.TextField()    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    comments = generic.GenericRelation(Comment, object_id_field="object_pk")
    
    @models.permalink
    def get_absolute_url(self):
        return ('blog.views.post_detail', [
            '%04d' % self.publish_date.year,
            '%02d' % self.publish_date.month,
            '%02d' % self.publish_date.day,
            self.slug,])
    
    objects = PostManager()
    published = PublishedPostManager()
    
    def save(self, *args, **kwargs):
        if (
            getattr(settings, 'BLOG_PING_GOOGLE', False) == True) \
            and (getattr(settings, 'DEBUG', True) == False):
            if self.is_published \
                and self.publish_date <= datetime.now():
                if not self.pk:
                    try:
                        ping_google()
                    except:
                        pass
                else:
                    old_post = Post.objects.get(pk=self.pk)
                    if old_post.is_published == False:
                        try:
                            ping_google()
                        except:
                            pass
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-publish_date',)
        get_latest_by = 'publish_date'
        
    def __unicode__(self):
        if self.is_published:
            return self.title
        else:
            return '%s (DRAFT)' % (self.title,)

    @property
    def post_categories_string(self):
        """
        Return the post categories in string format
        """
        return ', '.join([c.title for c in self.categories.all()])
            
    
    def get_previous_post(self):
        """
        Get the previous post by publish_date
        """
        return self.get_previous_by_publish_date(is_published=True,
            publish_date__lt=datetime.now)
 
    def get_next_post(self):
        """
        Get the next post by publish_date
        """
        return self.get_next_by_publish_date(is_published=True,
            publish_date__lt=datetime.now)
    
class PublishedPost(Post):
    """
    Published Post Proxy model
    """
    objects = PublishedPostManager()
    
    class Meta:
        proxy = True
    
class PostImage(models.Model):
    """
    Blog Post Image
    """
    post = models.ForeignKey(Post, related_name="images")
    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    image = models.ImageField(
        upload_to=lambda i,fn:'/'.join(
            ['apps', 'blogyall', 'images',
             i.post.publish_date.strftime('%Y-%m-%d'), i.post.slug, fn]
        ))
    gallery_position = models.PositiveIntegerField(blank=True, null=True,
        help_text="Post Images without a Gallery Position will not appear in " \
        "the post's gallery images")
    
    objects = PostImageManager()
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ('post', 'gallery_position', 'title',)

class PostModerator(CommentModerator):
    """
    Blog post comment moderator
    """
    enable_field='allow_comments'
    email_notification = getattr(settings, 'BLOG_COMMENTS_EMAIL_NOTIFICATION', False)
    if getattr(settings, 'BLOG_COMMENTS_AUTO_MODERATE', False):
        auto_moderate_field='publish_date'
        moderate_after=getattr(settings, 'BLOG_COMMENTS_MODERATE_AFTER', None)
    if getattr(settings, 'BLOG_COMMENTS_AUTO_CLOSE', False):
        auto_close_field='publish_date'
        close_after=getattr(settings, 'BLOG_COMMENTS_CLOSE_AFTER', None)

moderator.register(Post, PostModerator)
