from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image
import os


class CarouselItem(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='carousel/')
    order = models.PositiveIntegerField(default=0, help_text='Order in which this item appears in the carousel')
    link = models.URLField(blank=True, help_text='Optional link for the button')

    REQUIRED_WIDTH = 1920
    REQUIRED_HEIGHT = 1080

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()

    def resize_image(self):
        img_path = self.image.path
        image = Image.open(img_path)
        if image.width != self.REQUIRED_WIDTH or image.height != self.REQUIRED_HEIGHT:
            image = image.resize((self.REQUIRED_WIDTH, self.REQUIRED_HEIGHT), Image.Resampling.LANCZOS)
            image.save(img_path)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']

class AchievementItem(models.Model):
    title = models.CharField(max_length=255)
    icon_class = models.CharField(max_length=50, default="fa-heart")
    count = models.PositiveIntegerField()
    symbol = models.CharField(max_length=10, default='+')

    def __str__(self):
        return self.title