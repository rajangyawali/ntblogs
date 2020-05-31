from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import SignUpForm, EditProfileForm, ChangePasswordForm
from django.contrib import messages
from django.forms import modelform_factory
from django.forms import inlineformset_factory
from django.utils.text import slugify
from home.models import BlogPost, Author, PostImages, Subscriber


# Create your views here.
@login_required
def create(request):
    form = modelform_factory(BlogPost, fields=['title', 'image', 'description', 'featured', 'category', 'author'])
    if request.method == 'POST':
        form = form(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']            
            image = form.cleaned_data['image']
            description = form.cleaned_data['description']
            slug = slugify(title)
            featured = form.cleaned_data['featured']
            category = form.cleaned_data['category']
            author = form.cleaned_data['author']
            try:
                post = BlogPost(title=title, image=image, description=description, slug=slug, featured=featured,
                            category=category,author=author)
                post.save()
                post = get_object_or_404(BlogPost, slug=slug)
                if post.featured == 'True':                                 
                    subscribers = Subscriber.objects.all()
                    subscriber_list = [sub.subscriber for sub in subscribers]
                    message = '\n\n You can read the full post at \n http://ntblogs.herokuapp.com' +  str(post.get_absolute_url())
                    try:                        
                        send_mail(subject=title,message=message,from_email=settings.EMAIL_HOST_USER,
                                recipient_list=subscriber_list,fail_silently=False)
                    except:
                        pass
                messages.success(request, 'Your post has successfully been created !')
                return redirect('registration:posts')
            except:
                messages.error(request, 'Error submitting your post. The slug field is not unique. Please try again with another title !!')
                return render(request, 'registration/create_post.html', context={"form":form})    
        else:
            messages.error(request, 'Error submitting your post. Please try again with valid parameters !!')
            return render(request, 'registration/create_post.html', context={"form":form})
    return render(request, 'registration/create_post.html', context={"form":form})

@login_required
def add_images(request,slug):
    post = get_object_or_404(BlogPost, slug=slug)
    imageForm = modelform_factory(PostImages, fields=['post','image'])
    PostImagesFormSet = inlineformset_factory(BlogPost, PostImages, form=imageForm,max_num=6,extra=3)
    if request.method == 'POST':
        formset = PostImagesFormSet(request.POST, request.FILES, instance=post)
        if formset.is_valid():
            formset.save()
            return redirect('registration:posts')
    else:
        formset = PostImagesFormSet(instance=post)
        return render(request, 'registration/add_images.html', {"formset":formset})
    return render(request, 'registration/add_images.html', {"formset":formset})

@login_required
def posts(request):
    user = request.user
    posts = BlogPost.objects.filter(Q(author__first_name__contains=user.first_name) & Q(author__last_name__contains=user.last_name))
    return render(request, 'registration/list_posts.html', {'posts':posts})

@login_required
def edit(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    form = modelform_factory(BlogPost, fields=['title', 'image', 'description', 'featured', 'category', 'author'])
    form2 = form(instance=post)
    if request.method == 'POST':
        form = form(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully edited your post!')
            return redirect('registration:posts')
        else:
            messages.error(request, 'Error editing your post. Try again !!')
            return render(request, 'registration/edit_post.html', {'form':form2})
    return render(request, 'registration/edit_post.html', {'form':form2})

@login_required
def delete(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    post.delete()
    messages.success(request, 'You have successfully deleted your post !')
    posts = BlogPost.objects.all()
    return render(request, 'registration/list_posts.html', {'posts':posts})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('registration:posts')

        else:
            messages.success(request, 'Login Failed. Please, try again !')
            return redirect('registration:login')

    else:
        return render(request, 'registration/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out !')
    return redirect('registration:login')

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been edited and now logged in !')
            return redirect('registration:posts')
    else:
        form = EditProfileForm(instance = request.user)
    context = {'form':form}
    return render(request, 'registration/edit_profile.html', context)

def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(data = request.POST, user = request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password has been changed and now logged in !')
            return redirect('registration:posts')
    else:
        form = ChangePasswordForm(user = request.user)
    context = {'form':form}
    return render(request, 'registration/change_password.html', context)

