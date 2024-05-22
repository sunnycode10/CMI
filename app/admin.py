from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import CarouselItem, AchievementItem
from PIL import Image
import os

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
