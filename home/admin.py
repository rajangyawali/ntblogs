from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin
from . models import (Author, BlogPost, PostImages, Search, 
                        Contact, Advertisement, Subscriber, AuthorFollowLinks)

# Register your models here.

# class PostImagesAdmin(admin.TabularInline):
#     model = PostImages
#     extra = 1
#     max_num = 3

class BlogPostModelAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin, admin.ModelAdmin):
    # inlines = [PostImagesAdmin]
    list_display = ["title", "description","category", "featured", "author",  "posted", "updated"]
    list_display_links = ["description", "category", "author"]
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ["category", "featured", "author", "posted"]
    
    class Meta:
        model = BlogPost

class AuthorModelAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin, admin.ModelAdmin):
    class Meta:
        model = Author

class SearchModelAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin, admin.ModelAdmin):
    class Meta:
        model = Search

class ContactModelAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin, admin.ModelAdmin):
    class Meta:
        model = Contact

class AdvertisementModelAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin, admin.ModelAdmin):
    class Meta:
        model = Advertisement

class SubscriberModelAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin, admin.ModelAdmin):
    class Meta:
        model = Subscriber

class AuthorFollowLinksModelAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin, admin.ModelAdmin):
    class Meta:
        model = AuthorFollowLinks



admin.site.register(Author, AuthorModelAdmin)
admin.site.register(AuthorFollowLinks, AuthorFollowLinksModelAdmin)
admin.site.register(Search, SearchModelAdmin)
admin.site.register(Contact, ContactModelAdmin)
admin.site.register(Advertisement, AdvertisementModelAdmin)
admin.site.register(Subscriber, SubscriberModelAdmin)
admin.site.register(BlogPost, BlogPostModelAdmin)
# admin.site.register(PostImages, PostImagesModelAdmin)


