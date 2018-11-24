from ..settings import STATIC_URL
from ..local_settings import SITE_URL
from django import template
from sorl.thumbnail.templatetags.thumbnail import ThumbnailNode
from django.core.files.storage import FileSystemStorage


register = template.Library()


@register.filter()
def static_url(value):
    return ''.join([SITE_URL, STATIC_URL, value])


class StaticThumbnailStorage(FileSystemStorage):
    def __init__(self, *args, **kw):
        super(StaticThumbnailStorage, self).__init__(
            *args, location=SITE_URL,
            base_url=STATIC_URL, **kw)


storage = StaticThumbnailStorage()


class StaticThumbnailNode(ThumbnailNode):
    def _get_thumbnail(self, file_, geometry, **options):
        options['storage'] = storage
        return super(StaticThumbnailNode, self)._get_thumbnail(
                file_, geometry, **options)


@register.tag
def static_thumbnail(parser, token):
    return StaticThumbnailNode(parser, token)
