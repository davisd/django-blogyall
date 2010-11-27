from models import Post

from django.contrib.syndication.views import Feed

from django.core.urlresolvers import reverse

class PostFeed(Feed):
    """
    Post Feed
    """
    def __init__(self, link='/blog/', title='blog', description='the blog'):
        super(PostFeed, self).__init__()
        self.title = title
        self.link = link
        self.description = description
        
    def items(self):
        return Post.published.all()
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return item.content