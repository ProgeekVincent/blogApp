import random

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Contact, Subscriber
from taggit.models import Tag
from django.db.models import Count
from .forms import ContactForm, SubscriberForm
from django.contrib import messages
from django.core.mail import send_mail


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    template_name = 'blog/post/index.html'
    context = {
        'posts': posts,
        'tags': tag,
        'subscriberForm': SubscriberForm()
    }
    return render(request, template_name, context)


def detail_post(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='publish',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:3]
    template_name = 'blog/post/single.html'
    context = {
        'post': post,
        'similar_posts': similar_posts,
    }
    return render(request, template_name, context)


def about(request):
    context = None
    template_name = 'blog/about/about.html'
    return render(request, template_name, context)


def work(request):
    context = None
    template_name = 'blog/work/work.html'
    return render(request, template_name, context)


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your contact has been successfully received.")
        else:
            messages.error(request, "Your contact has been unsuccessfully received")
        return redirect('blog:contact')
    form = ContactForm()
    template_name = 'blog/contact/contact.html'
    context = {'form': form}
    return render(request, template_name, context)


def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)


# This is a newsletter view that sends mail to be confirmed
def new(request):
    if request.method == 'POST':
        data = Subscriber(email=request.POST['email'], conf_num=random_digits())
        data.save()
        send_mail(
            "Newsletter email confirmation.",
            "",
            "",
            [data.email],
            fail_silently=False,
            html_message="Well done in your first step.\
                        The second step is to confirm your email using this link" + " <a href='{}?email={}&conf_num={}'>\
                        click it</a> then you'll be redirected to the platform.".format(
                request.build_absolute_uri('confirm'),
                data.email,
                data.conf_num)
        )
        messages.success(request, "Congratulations on your first step." + \
                         "Your email " + data.email + " has been added." + \
                         "Please go to your email box and confirm your email address so that" + \
                         " so that you will receive the newsletters"
                         )
        return render(request, 'blog/post/confirmationMessage.html')
    # else:
    #     render(request, 'post/index.html', {'subscriberForm': SubscriberForm()})


def confirm(request):
    sub = Subscriber.objects.get(email=request.GET['email'])
    if sub.confirmed:
        messages.success(request, "Your email "+sub.email+" has been confirmed already")
        return render(request, 'blog/post/confirmationMessage.html')
    else:
        if sub.conf_num == request.GET['conf_num']:
            sub.confirmed = True
            sub.save()
            messages.success(request, "Congratulations your email "+sub.email+" has been confirmed. You will now "\
                                                                              "receive our newsletter.")
            return render(request, 'blog/post/confirmationMessage.html')


def delete(request):
    sub = Subscriber.objects.get(email=request.GET['email'])
    if sub.conf_num == request.GET['conf_num']:
        sub.delete()
        messages.success(request, "Your email "+sub.email+" has been unsubscribed from receiving our newsletters.")
        return render(request, 'blog/post/confirmationMessage.html')
    else:
        messages.error(request, "Unfortunately your email "+sub.email+" has not been removed to our subscription.")
        return render(request, 'blog/post/confirmationMessage.html')
