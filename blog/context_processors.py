from django.shortcuts import get_object_or_404
from django.http import Http404
import django.template.context

from tagging.models import Tag, TaggedItem

from models import Post, Series, Category

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
    def cp_wrapper(*args, **kwargs):
        if (
            len(args) == 1 and len(kwargs) == 0) \
            or (len(args) == 0 and len(kwargs) == 1 and 'request' in kwargs):
            return target(*args, **kwargs)
        else:
            def get_processor(request):
                return target(request, *args, **kwargs)
            return get_processor
    return cp_wrapper
            
@context_processor
def blog_posts_processor(request, year=None, month=None, category_slug=None,
    series_slug=None, tag=None, require_featured=False, start_post=1,
    max_posts=None,
    posts_context_name='posts',
    year_context_name='year', month_context_name='month',
    category_context_name='category', series_context_name='series',
    tag_context_name='tag'):
    """
    Return a dictionary containing:
    
    posts
    archive year (if supplied)
    archive month (if year and month supplied)
    category (if a slug was supplied)
    series (if a slug was supplied)
    tag (if a tag was supplied)
    
    """
    # is this user staff?  Determines published post display
    is_staff = request.user.is_staff
    posts = Post.objects.build_query(require_published = not is_staff,
        year=year, month=month, category_slug=category_slug,
        series_slug=series_slug, tag=tag, require_featured=require_featured)
    
    if max_posts != None:
        posts = posts[start_post-1:max_posts]
    elif start_post != None:
        posts = posts[start_post-1:]
            
    c = {
        posts_context_name: posts,
    }
    if year:
        c[year_context_name] = year
        if month:
            c[month_context_name] = month
    if category_slug:
        c[category_context_name] = get_object_or_404(
            Category, slug=category_slug)
    if series_slug:
        c[series_context_name] = get_object_or_404(Series, slug=series_slug)
    if tag:
        c[tag_context_name] = tag
    return c
        

@context_processor
def blog_post_processor(request, year, month, day, slug, context_name='post'):
    """
    Return a dictionary containing a post
    """
    # is this user staff?  Determines published post display
    is_staff = request.user.is_staff
    try:
        if is_staff:
            post = Post.objects.get(publish_date__year=year,
                publish_date__month=month, publish_date__day=day, slug=slug)
        else:
            post = Post.objects.get(is_published=True, publish_date__year=year,
                publish_date__month=month, publish_date__day=day, slug=slug)
            
        return {context_name: post}
    except Post.DoesNotExist:
        raise Http404
    
@context_processor
def blog_categories_processor(request, context_name='categories'):
    """
    Return a dictionary containing categories
    """
    return {context_name: Category.objects.all()}

@context_processor
def blog_category_processor(request, slug, context_name='category'):
    """
    Return a dictionary containing a category
    """
    # is this user staff?  Determines published post display
    is_staff = request.user.is_staff
    posts = Post.objects.build_query(
        require_published = not is_staff, category_slug=slug)
    try:        
        category = Category.objects.get(slug=slug)
        return{context_name: category}
    except Category.DoesNotExist:
        raise Http404
    
@context_processor
def blog_seriess_processor(request, context_name='seriess'):
    """
    Return a dictionary containing seriess
    """
    return {context_name: Series.objects.all()}

@context_processor
def blog_series_processor(request, slug, context_name='series'):
    """
    Return a dictionary containing a series
    """
    # is this user staff?  Determines published post display
    is_staff = request.user.is_staff
    posts = Post.objects.build_query(
        require_published = not is_staff, series_slug=slug)
    try:
        series = Series.objects.get(slug=slug)
        return {context_name: series}
    except Series.DoesNotExist:
        raise Http404

@context_processor
def blog_tags_processor(request, context_name='tags'):
    """
    Return a dictionary containing tags
    """
    return {
        context_name: Tag.objects.usage_for_model(Post)
    }

@context_processor
def blog_tag_processor(request, tag, context_name='tag'):
    """
    Return a dictionary containing a tag
    """
    return {
        context_name: get_object_or_404(Tag, name=tag),
        }
