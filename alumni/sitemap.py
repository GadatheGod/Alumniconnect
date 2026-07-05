from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from alumni.models import AlumniProfile


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['home', 'register', 'directory']

    def location(self, item):
        return reverse(item)


class AlumniProfileSitemap(Sitemap):
    priority = 0.6
    changefreq = 'monthly'

    def items(self):
        return AlumniProfile.objects.all()

    def lastmod(self, obj):
        return obj.updated_at