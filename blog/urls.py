from django.conf.urls.shortcut import patterns

from syndication import PostFeed

urlpatterns = patterns('blog.views',
    (r'^$', 'post_index'),
    (r'^rss/$', PostFeed(title='Blog', link="/", description="Blog")),
    (r'^archive/$', 'post_archive'),
    (r'^(?P<year>\d{4})/$', 'post_archive'),
    (r'^(?P<year>\d{4})/(?P<month>0[1-9]|1[0-2])/$', 'post_archive'),
    (r'^latest/$', 'post_index', {'start_post':1, 'max_posts':3}),
    (r'^categories/$', 'category_index'),
    (r'^categories/(?P<category_slug>[-\w]+)/(?P<year>\d{4})/$', 'post_index'),
    (r'^categories/(?P<category_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>0[1-9]|1[0-2])/$', 'post_index'),
    (r'^categories/(?P<slug>[-\w]+)/$', 'category_detail'),
    (r'^series/$', 'series_index'),
    (r'^series/(?P<series_slug>[-\w]+)/(?P<year>\d{4})/$', 'post_index'),
    (r'^series/(?P<series_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>0[1-9]|1[0-2])/$', 'post_index'),
    (r'^series/(?P<slug>[-\w]+)/$', 'series_detail'),
    (r'^tags/$', 'tag_index'),
    (r'^tags/(?P<tag>[-\w]+)/(?P<year>\d{4})/$', 'post_index'),
    (r'^tags/(?P<tag>[-\w]+)/(?P<year>\d{4})/(?P<month>0[1-9]|1[0-2])/$', 'post_index'),
    (r'^tags/(?P<tag>.+)/$', 'tag_detail'),
    (r'^(?P<year>\d{4})/(?P<month>0[1-9]|1[0-2])/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 'post_detail'),
)
