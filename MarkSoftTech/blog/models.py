from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
from django.core.mail import send_mail


# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='publish')



class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('publish', 'Publish')
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                            unique_for_date='created')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30,
                              choices=STATUS_CHOICES,
                              default='draft')
    object = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ('-title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[
                           self.publish.year,
                           self.publish.month,
                           self.publish.day,
                           self.slug
                       ])




    def send(self, request):
        subscribers = Subscriber.objects.filter(confirmed=True)
        for subscriber in subscribers:
            send_mail(
                self.title,
                "",
                "",
                [subscriber],
                fail_silently=False,
                html_message=self.body + ". To visit this post on our website click this <a href='{}?email={}&conf_num{}'>link.</a>".format(
                    request.build_absolute_uri(self.get_absolute_url()),
                    subscriber.email,
                    subscriber.conf_num
                ) + 'You can unsubscribe to our newsletters click this <a href="{}?email={}&conf_num{}">link.</a>'.format(
                    request.build_absolute_uri('delete'),
                    subscriber.email,
                    subscriber.conf_num
                )
            )


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=250)
    website = models.CharField(blank=True, max_length=400)
    location = models.CharField(blank=True, max_length=500)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    publish = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "SUBJECT : " + self.subject


class Subscriber(models.Model):
    email = models.EmailField()
    conf_num = models.CharField(max_length=200)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.email + "(" + ("not " if not self.confirmed else "") + "confirmed)"
