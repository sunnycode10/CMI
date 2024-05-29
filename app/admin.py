from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import CarouselItem, AchievementItem, Newsletter
from PIL import Image
import os
import csv
from django.http import HttpResponse
from django.contrib import admin


@admin.register(CarouselItem)
class CarouselItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'image_tag', 'image_dimensions')
    ordering = ('order',)
    readonly_fields = ('image_dimensions',)

    def image_tag(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" style="width: 100px; height: auto;" />')
    image_tag.short_description = 'Image'

    def image_dimensions(self, obj):
        if obj.image:
            try:
                image = Image.open(obj.image.path)
                return f'{image.width} x {image.height}'
            except FileNotFoundError:
                return 'File not found'
        return 'No image'
    image_dimensions.short_description = 'Dimensions'

@admin.register(AchievementItem)
class CAchievementItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_class', 'count', 'symbol')




class NewsletterAdmin(admin.ModelAdmin):
    list_filter = ['has_made_donation']
    list_display = ['email', 'has_made_donation']
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=newsletter.csv'
        writer = csv.writer(response)
        writer.writerow(['Email', 'Has Made Donation'])
        for obj in queryset:
            writer.writerow([obj.email, obj.has_made_donation])
        return response
    export_as_csv.short_description = "Export Selected to CSV"

admin.site.register(Newsletter, NewsletterAdmin)