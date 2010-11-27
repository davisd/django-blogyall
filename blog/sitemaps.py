from django.contrib.sitemaps import Sitemap
from models import Post, Category, Series

class PostSitemap(Sitemap):
    """
    Post sitemap
    """
    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.last_modified
    
class CategorySitemap(Sitemap):
    """
    Category sitemap
    """
    def items(self):
        return Category.objects.all()
    
class SeriesSitemap(Sitemap):
    """
    Series sitemap
    """
    def items(self):
        return Series.objects.all()

    def lastmod(self, obj):
        return obj.created_on
