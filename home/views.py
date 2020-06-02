from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import Q
from django.db import models
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from . models import Author, BlogPost, Search, Contact, Advertisement, Subscriber, PostImages
from .forms import ContactForm, SubscriberForm
from django.forms import modelform_factory

flag = 0
PAGINATION_NUMBER = 8
categories = {'Technology' :1, 'Politics' : 2, 'Society' : 3, 'Economics' : 4, 'Education' : 1, 'Tourism' : 2,
                'Development' : 3,'Food' : 4, 'Fashion' : 1, 'Health' : 2, 'Entertainment' : 3, 'International' : 4}

def main_adv():
    return Advertisement.objects.all().filter(type='Main')

def side_adv():
    return Advertisement.objects.all().filter(type='Side')    

def categories_counts(posts):
    post_categories = [post.category for post in posts]
    categories_count = [post_categories.count(key) for key in categories.keys()] 
    return zip(categories.keys(), categories.values(), categories_count)

def popular_posts_details():
    popular_posts_details = BlogPost.objects.order_by('-hit_count_generic__hits')
    popular_posts_details = popular_posts_details[:4]
    popular_posts_details_categories = [post.category for post in popular_posts_details]
    popular_posts_details_colors = [categories[category] for category in popular_posts_details_categories]
    return zip(popular_posts_details, popular_posts_details_colors)

def home(request):
    # Code for newsletter subscription from subscribers. This will write 
    # valid email addresses to our Subscriber model
    if request.method == "POST":
        form = SubscriberForm(request.POST)
        if form.is_valid():
            subscriber = form.cleaned_data['subscriber']
            try:
                send_mail(subject="Subscription", 
                        message="You have successfully subscribed our newsletter. \n\nYou will get recent updates of our featured news.\n\nRegards:\nNT Blogs Team",
                        from_email=settings.EMAIL_HOST_USER, recipient_list=[subscriber], fail_silently=False)   
            except:
                pass
            try:
                subscriber = Subscriber(subscriber=subscriber)
                subscriber.save()
                messages.success(request, 'Your have successfully subscribed our newsletter. You will be getting most recent updates of our featured news. Thank you !!')
            except:
                messages.error(request, 'Error subscribing newsletter. You have already subscribed !!')
        else:
            messages.error(request, 'Error subscribing newsletter. Please, try again with valid email address !!')    
    
    # Code for fetching all posts in the home page
    posts = BlogPost.objects.all()
    featured_posts = posts.filter(featured = 'True')[:3]
    # Code for showing posts category counts and their colors
    categories_colors_counts = categories_counts(posts)

    # Code for showing category of each post and their category color
    post_categories = [post.category for post in posts]
    colors = [categories[category] for category in post_categories]  
    featured_post_categories = [post.category for post in featured_posts]
    featured_colors = [categories[category] for category in featured_post_categories]   
    
    hero_posts = zip(posts[0:2], colors[0:2])    
    recent_posts = zip(posts[2:8], colors[2:8])
    sub_hero_posts = zip(posts[8:9], colors[8:9])
    sub_posts = zip(posts[9:15], colors[9:15])
    featured_posts = zip(featured_posts, featured_colors)

    context = {
        'hero_posts':hero_posts,
        'recent_posts':recent_posts,
        'sub_hero_posts':sub_hero_posts,
        'sub_posts':sub_posts,
        'featured_posts':featured_posts,
        'categories_colors_counts':categories_colors_counts,
        'popular_posts': BlogPost.objects.order_by('-hit_count_generic__hits')[:12],
        'popular_posts_details':popular_posts_details(),
        'main_adv':main_adv(),
        'side_adv':side_adv(),
        'form':SubscriberForm()
    }
    return render(request, 'home/index.html', context)

def details(request, slug):
    global flag
    if flag == 0:    
        posts = BlogPost.objects.all()
        my_posts = posts
    else:
        posts = my_posts
        flag = 1
    print(flag)
    categories_colors_counts = categories_counts(posts)
    count_hit=True
    post = get_object_or_404(BlogPost, slug = slug)
    hit_count = HitCount.objects.get_for_object(post)
    hit_count_response = HitCountMixin.hit_count(request, hit_count)

    context={
        'post':post,
        'categories_colors_counts':categories_colors_counts,
        'popular_posts': BlogPost.objects.order_by('-hit_count_generic__hits')[:10],
        'main_adv':main_adv(),
        'side_adv':side_adv(),
        }
    return render (request, 'home/post-details.html', context)


def posts(request, category):
    all_posts = BlogPost.objects.all()
    search_query = request.GET.get('q','')
    search_message=''
    page_range=''
    if search_query:
        searched_posts = all_posts.filter(Q(title__icontains = search_query))
        posts = searched_posts
        search = Search(user=request.user, search=search_query)
        search.save()
        if not posts:
            search_message = '<i> No results found for your search query !! </i>'
    else:
        if category == 'posts':
            posts = all_posts
        elif category == 'popular':
            posts = BlogPost.objects.order_by('-hit_count_generic__hits')
        else:
            posts = all_posts.filter(category = category)

    paginator = Paginator(posts, PAGINATION_NUMBER)
    page = request.GET.get('page',1)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(PAGINATION_NUMBER)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    index = posts.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range)[start_index:end_index]

    categories_colors_counts = categories_counts(all_posts)

    post_categories = [post.category for post in posts]
    colors = [categories[category] for category in post_categories]
    posts_colors = zip(posts, colors) 
    context={
        'category':category,
        'posts_colors':posts_colors,
        'posts':posts,
        'query':search_query,
        'page_range':page_range,
        'categories_colors_counts':categories_colors_counts,
        'search_message':search_message,
        'popular_posts': BlogPost.objects.order_by('-hit_count_generic__hits')[:10],
        'main_adv':main_adv(),
        'side_adv':side_adv()
    }
    return render(request, 'home/posts.html', context)



def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']            
            message = form.cleaned_data['message']
            contact = Contact(email=email, subject=subject, message=message)
            contact.save()
            messages.success(request, 'Your message has been sent. Thank you !!')
            return redirect('home')
        else:
            messages.error(request, "Error sending message !")
            return render(request, "home/contact.html", context={"form":form})

    return render(request, 'home/contact.html', context={"form":form})

def about(request):
    context ={
        'popular_posts': BlogPost.objects.order_by('-hit_count_generic__hits')[:10],
        'authors': Author.objects.all(),
        'main_adv':main_adv(),
        'side_adv':side_adv()
    }
    return render(request, 'home/about.html', context)

def advertisement(request):    
    context = {
        'main_adv':main_adv(),
        'side_adv':side_adv()
    }
    return render(request, 'home/advertisement.html', context)

def join(request):    
    context = {
        'main_adv':main_adv(),
        'side_adv':side_adv()
    }
    return render(request, 'home/join.html', context)

def privacy(request):
    return render(request, 'home/privacy.html')

def error_404(request, exception):
    return render(request, 'error_404.html', status='404')

def error_500(request):
    return render(request, 'error_500.html', status='500')
