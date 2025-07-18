from django.contrib import admin
from .models import SourceType, Source, Quote


class SourceTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('name',)
    date_hierarchy = 'created_at'


class QuoteAdmin(admin.ModelAdmin):
    list_display = ('short_text', 'source', 'weight', 'popularity', 'views')
    list_filter = ('source', 'source__type')
    search_fields = ('text',)
    readonly_fields = ('views', 'likes', 'dislikes')
    fieldsets = (
        (None, {
            'fields': ('text', 'source', 'weight')
        }),
        ('Статистика', {
            'fields': ('views', 'likes', 'dislikes'),
            'classes': ('collapse',)
        }),
    )

    def short_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    short_text.short_description = 'Текст'


admin.site.register(SourceType, SourceTypeAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Quote, QuoteAdmin)