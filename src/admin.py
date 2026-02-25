from django.contrib import admin
from django.utils.html import format_html

from src.models import Site, Article


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'url')

    def get_fields(self, request, obj=None):
        if request.user.is_superuser:
            return  'name', 'url', 'is_active', 'proxy'
        return  'name', 'url'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('linked_title', 'subtitle', 'site__name', 'published_at')
    ordering = ('-published_at',)
    list_filter = ('site__name', 'published_at', 'created_at')
    show_facets = admin.ShowFacets.ALWAYS

    def linked_title(self, obj):
        # Возвращает HTML ссылку
        return format_html('<a href="{}" target="_blank">{}</a>', obj.url, obj.title)
    linked_title.short_description = 'Title'

# base_url = models.URLField(unique=True)
#     name = models.CharField(max_length=255)
#     is_active = models.BooleanField(default=True)
#     scraping_type = models.CharField(max_length=50, choices=ScrapingType.choices, default=ScrapingType.REQUEST)
# https://www.epo.org/en/news-events/news
# https://nipo.gov.ua/blog/page/{page}/
