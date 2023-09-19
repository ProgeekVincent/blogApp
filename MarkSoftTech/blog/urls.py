
from django.urls import path
from .views import (post_list, detail_post, about, work, contact, new, confirm, delete)

app_name = 'blog'


urlpatterns = [
    path('', post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>', detail_post, name='post_detail'),
    path('about',about, name='about'),
    path('work', work, name='work'),
    path('contact', contact, name='contact'),
    path('new', new, name='new'),
    path('confirm', confirm, name='confirm'),
    path('delete', delete, name='delete'),
]
