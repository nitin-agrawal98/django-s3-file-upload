from django.contrib import admin
from upload_file.models import Profile, ProfileImage

# Register your models here.
class ProfileImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_tag', )
    readonly_fields = ['image_tag', ]

class ProfileImageInline(admin.TabularInline):
    model = ProfileImage
    list_display = ('title', 'image_tag', )
    readonly_fields = ['image_tag', ]
    extra = 0

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', )
    inlines = [ProfileImageInline]

    def save_model(self, request, obj, form, change):
        obj.save()
        for image in request.FILES.getlist('images_multiple'):
            profile_image = ProfileImage(profile=obj, image=image, title=image.name)
            profile_image.save()

    def delete_model(self, request, obj):
        profile_images = obj.images.all()
        for profile_image in profile_images:
            profile_image.delete()
        obj.delete()

    def delete_queryset(self, request, queryset):
        for profile in queryset:
            profile_images = profile.images.all()
            for profile_image in profile_images:
                profile_image.delete()
        queryset.delete()

admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProfileImage, ProfileImageAdmin)
