from django.db import models

from django.utils.html import format_html

from django_s3.settings import AWS_FOLDER_NAME

# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ProfileImage(models.Model):
    title = models.CharField(max_length=100)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='images')
    image = models.FileField(upload_to=AWS_FOLDER_NAME)

    def image_tag(self):
        return format_html('<img src="{url}" width="50" height="50" />'.format(
            url = self.image.url
        ))
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def delete(self):
        self.image.delete()
        super().delete()
    
    def __str__(self):
        return self.title