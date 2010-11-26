from django.http import HttpResponse, Http404
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response, get_object_or_404

from tagging.models import Tag, TaggedItem

from models import Post, Category, Series

from context_processors import blog_posts_processor, blog_post_processor, \
    blog_categories_processor, blog_category_processor, \
    blog_seriess_processor, blog_series_processor, \
    blog_tags_processor, blog_tag_processor
     

def post_index(request, year=None, month=None, category_slug=None,
    series_slug=None, tag=None, start_post=1, max_posts=None,
    template_name="blog/post/index.html"):
    """
    Post Index
    """
    return render_to_response(
        template_name,
        context_instance=RequestContext(
            request,
            processors=[blog_posts_processor(year=year, month=month,
                category_slug=category_slug, series_slug=series_slug,
                tag=tag, start_post=start_post, max_posts=max_posts),]
        )
    )

def post_archive(request, year=None, month=None,
    template_name="blog/post/archive.html"):
    """
    Post Index
    """
    return render_to_response(
        template_name,
        context_instance=RequestContext(
            request,
            processors=[blog_posts_processor(year=year, month=month),]
        )
    )

def post_detail(request, year, month, day, slug,
    template_name="blog/post/detail.html"):
    """
    Post Detail
    """
    return render_to_response(
        template_name,
        context_instance=RequestContext(
            request,
            processors=[blog_post_processor(year=year, month=month, day=day,
                slug=slug),]
        )
    )

def category_index(request, template_name="blog/category/index.html"):
    """
    Category Index
    """
    return render_to_response(
        template_name,
        context_instance=RequestContext(
            request,
            processors=[blog_categories_processor,]
        )
    )

def category_detail(request, slug, template_name="blog/category/detail.html"):
    """
    Category Detail
    """
    return render_to_response(
        template_name,
        context_instance=RequestContext(
            request,
            processors=[blog_category_processor(slug=slug),]
        )
    )

def series_index(request, template_name="blog/series/index.html"):
    """
    Series Index
    """
    return render_to_response(
        template_name,
        context_instance=RequestContext(
            request,
            processors=[blog_seriess_processor,]
        )
    )

def series_detail(request, slug, template_name="blog/series/detail.html"):
    """
    Series Detail
    """
    return render_to_response(
        template_name,
        context_instance=RequestContext(
            request,
            processors=[blog_series_processor(slug=slug),]
        )
    )

def tag_index(request, template_name="blog/tag/index.html"):
    """
    Tag Index
    """
    return render_to_response(
        template_name,
        context_instance=RequestContext(
            request,
            processors=[blog_tags_processor,]
        )
    )

def tag_detail(request, tag, template_name="blog/tag/detail.html"):
    """
    Tag Detail
    """
    return render_to_response(
        template_name,
        context_instance=RequestContext(
            request,
            processors=[blog_tag_processor(tag=tag),]
        )
    )

