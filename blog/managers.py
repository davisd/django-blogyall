from datetime import datetime

from django.db import models

from tagging.models import Tag, TaggedItem

class PostImageManager(models.Manager):
    """
    Post Image Manager
    """
    # use for related fields
    use_for_related_fields = True
    def get_gallery_images(self):
        """
        Get gallery images
        
        Gallery images are PostImages that have a non-null gallery position
        """
        return self.get_query_set().filter(gallery_position__isnull=False)
    
class PostManager(models.Manager):
    """
    Post Manager
    """
    # use for related fields
    use_for_related_fields = True
    def build_query(self, require_published=True, year=None, month=None,
        category_slug=None, series_slug=None, tag=None, require_featured=False):
        # Initial posts by require published indicator
        if require_published:
            posts = self.get_query_set().filter(is_published=True,
                publish_date__lt=datetime.now)
        else:
            posts = self.get_query_set()
            
        # featured
        if require_featured == True:
            posts = posts.filter(is_featured=True)
            
        # date
        if year:
            posts = posts.filter(publish_date__year=year)
            if month:
                posts = posts.filter(publish_date__month=month)
                
        #category and series
        if category_slug:
            posts = posts.filter(categories__slug=category_slug)
        if series_slug:
            posts = posts.filter(series__slug=series_slug)
            
        # tag
        if tag:
            # return posts filtered by the tag
            return TaggedItem.objects.get_by_model(posts, [tag,])
        else:
            return posts
    
    def get_published_posts(self):
        """
        Get published posts
        """
        return self.build_query(require_published=True)

            
    def get_featured_posts(self):
        """
        Get featured posts
        """
        return self.build_query(require_published=True, require_featured=True)
    
    def get_post_archive(self, require_published=True, year=None, month=None,
        category_slug=None, tag=None):
        """
        Return a Post Archive
        
        A blog post archive is a tuple of (year, months[]),
        each month containing a tuple of (month, days[]),
        each day containing a tuple of (day, posts[])
        
        """
        # This was originally done as a dictionary
        # but python dictionaries can't guarantee sort order.
        posts = self.build_query(require_published=require_published, year=year,
            month=month, category_slug=category_slug, tag=tag)
        post_archive = {}
        for post in posts.order_by('-publish_date'):
            if not post_archive.has_key(post.publish_date.year):
                post_archive[post.publish_date.year] = {}
            if not post_archive[post.publish_date.year].has_key(post.publish_date.month):
                post_archive[post.publish_date.year][post.publish_date.month] = {}
            if not post_archive[post.publish_date.year][post.publish_date.month].has_key(post.publish_date.day):
                post_archive[post.publish_date.year][post.publish_date.month][post.publish_date.day] = []
            post_archive[post.publish_date.year][post.publish_date.month][post.publish_date.day].append(post)

        # Now that all of that lifting is done, convert the dictionaries into tuples with lists
        sorted_years = [(k,[]) for k in sorted(post_archive.keys(),
            reverse=True)]
        for sorted_year in sorted_years:
            sorted_months = [(k,[]) for k in sorted(post_archive[sorted_year[0]],
                reverse=True)]
            sorted_year[1].extend(sorted_months)
            for sorted_month in sorted_months:
                sorted_days = [(k,[]) for k in sorted(
                    post_archive[sorted_year[0]][sorted_month[0]], reverse=True)]
                sorted_month[1].extend(sorted_days)
                for sorted_day in sorted_days:
                    sorted_day[1].extend(
                        post_archive[sorted_year[0]][sorted_month[0]][sorted_day[0]])
            
        return sorted_years
    
    @classmethod
    def get_tags_in_use(cls):
        """
        Return the tags in use
        """
        return Tag.objects.filter(
            id__in=TaggedItem.objects.filter(
                content_type=ContentType.objects.get(
                    app_label='blogyall',
                    model=cls
                )
            ).values('tag_id')
        )

class PublishedPostManager(PostManager):
    """
    Published Post Manager
    """
    def get_query_set(self):
        return super(PublishedPostManager, self).get_query_set().filter(is_published=True)
    