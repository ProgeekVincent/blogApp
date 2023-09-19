from django.contrib import admin
from .models import Post, Contact, Subscriber

#newsletter send method
def send_newsletter(modelAdmin, request, queryset):
    for newsletter in queryset:
        newsletter.send(request)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug' : ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    actions = [send_newsletter]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'website' , 'location', 'subject', 'message')
    list_filter = ('subject', 'location', 'publish')
    date_hierarchy = 'publish'
    ordering = ('publish', 'location')

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'confirmed')