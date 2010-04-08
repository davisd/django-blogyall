import re

from django import template
import django.core.urlresolvers
from django.db import models
from django.utils import dates

from tagging.models import TaggedItem

from blog.models import Post, Category

register = template.Library()

def lit_or_val(var, context):
    """
    Returns a literal string or numeric value, or the value of the Variable resolved from the context
    """
    if var == None:
        return None
    if var[0] == var[-1] and var[0] in ('"', "'"):
        if len(var) < 3:
            return '' # empty string
        else:
            return var[1:-1] # string
    else:
        try:
            return float(var)
        except ValueError:
            return template.Variable(var).resolve(context) # resolve value

class BlogCategoriesNode(template.Node):
    def __init__(self, var_name):
        self.args = dict(var_name=var_name)
    def render(self, context):
        var_name = self.args['var_name']
        context[var_name] = Category.objects.all()
        return ''

class BlogTagPostsNode(template.Node):
    def __init__(self, tag, var_name):
        self.args = dict(tag=tag, var_name=var_name)
    def render(self, context):
        tag = lit_or_val(self.args['tag'], context)
        var_name = self.args['var_name']
        context[var_name] = TaggedItem.objects.get_by_model(Post.objects.get_published_posts(), tag)
        return ''
    
class PostArchiveNode(template.Node):
    def __init__(self, var_name, year=None, month=None):
        self.args = dict(var_name=var_name, year=year, month=month)        
    def render(self, context):
        var_name = self.args['var_name']
        year = lit_or_val(self.args['year'], context)
        month = lit_or_val(self.args['month'], context)
        context[var_name] = Post.objects.get_post_archive(year=year, month=month)
        return ''

def do_get_blog_tag_posts(parser, token):
    """
    Gets the blog Posts for a specified tag and stores it in a context variable.
    
    Usage::

      {% get_blog_tag_posts [tag_name] as [varname] %}
    
    tag should be a variable or a quoted string
    TODO: Use the "for" word...

    Example::
    
      {% get_blog_tag_posts "django" as blog_posts %}
    
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    tag, var_name = m.groups()
    return BlogTagPostsNode(tag, var_name)

def do_get_blog_post_archive(parser, token):
    """
    Returns a blog post archive
    
        A blog post archive is a tuple of (year, months[]), each month containing a tuple of
        (month, days[]), each day containing a tuple of (day, posts[])
    """
    args = token.split_contents()
    if args[-2] != 'as':
        raise template.TemplateSyntaxError, "incorrect parameters. format is %r [year] [month] as variable_name" % args[0]
    var_name = args[-1]
    year = None
    month = None
    if len(args) > 3:
        year = args[1]
    if len(args) > 4:
        month = args[2]
    if len(args) > 5:
        raise template.TemplateSyntaxError, "incorrect parameters. format is %r [year] [month] as variable_name" % args[0]
    return PostArchiveNode(var_name, year, month)

def do_get_blog_categories(parser, token):
    """
    Gets the blog Categories and stores them in a context variable
    
    Usage::
    
      {% get_blog_categories as [var_name] %}
      
    Example::
    
      {% get_blog_categories as blog_categories %}
    
    """
    args = token.split_contents()
    if args[-2] != 'as' or len(args) != 3:
        raise template.TemplateSyntaxError, "incorrect parameters. format is %r as variable_name" % args[0]
    var_name = args[-1]
    return BlogCategoriesNode(var_name)

def month_name(value):
    """
    Gets the month name from a numeric value
    
    Example::
       {{ Post.publish_date|month_name }}
    
    """
    return dates.MONTHS[int(value)]

def blog_tag_get_absolute_url(tag):
    """
    Gets an absolute_url from a tag as it relates to a blog post.
    
    Usage::

      {% blog_tag_get_absolute_url [tag] %}
    
    tag should be a variable or a quoted string
    TODO: Check that the quoted string thing works...
    
    Example::
    
      {% blog_tag_get_absolute_url "django" %}
    
    """
    return django.core.urlresolvers.reverse('blog.views.tag_detail', kwargs={'tag': tag})

register.tag('get_blog_tag_posts', do_get_blog_tag_posts)
register.tag('get_blog_post_archive', do_get_blog_post_archive)
register.tag('get_blog_categories', do_get_blog_categories)

register.simple_tag(blog_tag_get_absolute_url)

register.filter('month_name', month_name)