from models import Post, Series, Category
from tagging.models import Tag, TaggedItem
from django.shortcuts import get_object_or_404
from django.http import Http404

import inspect
import django.template.context

def context_processor(target):
    """
    Decorator that allows context processors with parameters to
    be assigned (and executed properly) in a RequestContext

    Example::

      return render_to_response(
        template_name,
        context_instance=RequestContext(
          request,
          processors=[
            test_processor1,
            test_processor2(val1=test_val1, val2=test_val2),
          ]
        )
      )
      
    """
    def wrapper(*args, **kwargs):
        # hack implementation
        caller_stack = inspect.stack()[1]
        module = inspect.getmodule(caller_stack[0])
        if module == django.template.context:
            return target(*args, **kwargs)
        else:
            def get_processor(request):            
                return target(request, *args, **kwargs)
            return get_processor
    return wrapper


@context_processor
def blog_posts_processor(request, year=None, month=None, category_slug=None, series_slug=None, tag=None, require_featured=False, start_post=1, max_posts=None):
    """
    Accepts Post attribute configurations for matching and
    returns a dictionary containing:
    
    blog_posts
    blog_posts_archive_year (if supplied)
    blog_posts_archive_month (if supplied)
    blog_category (if a slug was supplied)
    blog_series (if a slug was supplied)
    blog_tag (if a tag was supplied)
    
    """
    # is this user staff?  Determines published post display
    is_staff = request.user.is_staff
    posts = Post.objects.build_query(require_published = not is_staff, year=year, month=month, category_slug=category_slug, series_slug=series_slug, tag=tag, require_featured=require_featured)
    
    if max_posts != None:
        posts = posts[start_post-1:max_posts]
    elif start_post != None:
        posts = posts[start_post-1:]
            
    c = {
        'blog_posts': posts,
    }
    if year:
        c['blog_posts_archive_year'] = year
        if month:
            c['blog_posts_archive_month'] = month
    if category_slug:
        c['blog_category'] = get_object_or_404(Category, slug=category_slug)
    if series_slug:
        c['blog_series'] = get_object_or_404(Series, slug=series_slug)
    if tag:
        c['blog_tag'] = tag
    return c
        

@context_processor
def blog_post_processor(request, year, month, day, slug):
    """
    Blog post processor
    Returns a dictionary containing: blog_post
    """
    # is this user staff?  Determines published post display
    is_staff = request.user.is_staff
    try:
        if is_staff:
            post = Post.objects.get(publish_date__year=year, publish_date__month=month, publish_date__day=day, slug=slug)
        else:
            post = Post.objects.get(is_published=True, publish_date__year=year, publish_date__month=month, publish_date__day=day, slug=slug)
            
        return {'blog_post': post}
    except Post.DoesNotExist:
        raise Http404
    
@context_processor
def blog_categories_processor(request):
    """
    Categories processor
    Returns a dictionary containing: blog_categories
    """
    return {'blog_categories': Category.objects.all()}

@context_processor
def blog_category_processor(request, slug):
    """
    Category processor
    Returns a dictionary containing: blog_category
    """
    # is this user staff?  Determines published post display
    is_staff = request.user.is_staff
    posts = Post.objects.build_query(require_published = not is_staff, category_slug=slug)
    try:        
        category = Category.objects.get(slug=slug)
        return{'blog_category': category, 'blog_posts': posts}
    except Category.DoesNotExist:
        raise Http404
    
@context_processor
def blog_seriess_processor(request):
    """
    Seriess processor
    Returns a dictionary containing: blog_seriess
    """
    return {'blog_seriess': Series.objects.all()}

@context_processor
def blog_series_processor(request, slug):
    """
    Series processor
    Returns a dictionary containing: blog_series
    """
    # is this user staff?  Determines published post display
    is_staff = request.user.is_staff
    posts = Post.objects.build_query(require_published = not is_staff, series_slug=slug)
    try:
        series = Series.objects.get(slug=slug)
        return {'blog_series': series, 'blog_posts': posts}
    except Series.DoesNotExist:
        raise Http404

@context_processor
def blog_tags_processor(request):
    """
    Tags processor
    Returns a dictionary containing: blog_tags
    """
    return {
        'blog_tags': Tag.objects.usage_for_model(Post)
    }

@context_processor
def blog_tag_processor(request, tag):
    """
    Tag processor
    Returns a dictionary containing: blog_tag, blog_posts
    """
    # is this user staff?  Determines published post display
    is_staff = request.user.is_staff
    if not is_staff:
        blog_posts = TaggedItem.objects.get_by_model(Post.objects.get_published_posts(), [tag,])
    else:
        blog_posts = TaggedItem.objects.get_by_model(Post.objects.all(), [tag,])
    return {
        'blog_tag': get_object_or_404(Tag, name=tag),
        'blog_posts': blog_posts,
        }