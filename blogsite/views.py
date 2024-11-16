from django.shortcuts import render, redirect
from django.utils.text import slugify
from blogsite.models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import  authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .form import UserUpdateForm, ProfileUpdateForm, PostForm, CommentForm
from django.shortcuts import get_object_or_404



# Create your views here.

def home(request):
    return render(request, "blogsite/home.html")

@login_required(login_url='login')
def post_create(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        data = request.POST
        title = data.get('title')
        content = data.get('content')
        category_id = request.POST['category']
        is_published = 'is_published' in request.POST
        
        category = Category.objects.get(id=category_id)
        image = request.FILES.get('image')

        post = Post.objects.create(
            title=title,
            slug=slugify(title),
            content=content,
            author=request.user,
            category=category,
            image = image,
            is_published=is_published
        )
        print(data)
        post.save()
        return redirect('blog-home')  # Redirect to the home page or post detail page

    return render(request, 'blogsite/post.html', {'categories': categories})


def home(request):
    posts = Post.objects.all().order_by('-created_at')  # Fetch posts, ordered by date
    return render(request, 'blogsite/home.html', {'posts': posts})

def single_post(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all().order_by('-created_at')  # Fetch comments for the post
    comment_form = CommentForm()

    if request.method == "POST" and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('single', id=post.id)

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'blogsite/single.html', context)


def login_task(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        
        # Check if the user exists
        if not User.objects.filter(username=username).exists():
            messages.info(request, "Invalid username")
            return redirect('login')
        
        # Authenticate user
        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request, "Invalid password")
            return redirect('login')
        else:
            login(request, user)
            return redirect('blog-home')  # Redirect to task page on successful login

    return render(request, 'blogsite/login.html')


def reg_task(request):
    if request.method == 'POST':
        data = request.POST
        fullname = data.get('fullname')
        username = data.get('username')
        password = data.get('password')

        u = User.objects.filter(username=username)

        if u.exists():
            messages.info(request, "User name already exist")
            return redirect('register')

        user = User.objects.create(
            username = username,
            first_name = fullname
            )
        user.set_password(password)
        user.save()

        messages.info(request, "Account created")
        redirect('login')
        
    return render(request, 'blogsite/reg.html')


def logout_page(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')  # Fetch user's posts
    
    context = {
        "u_form": u_form,
        "p_form": p_form,
        "user_posts": user_posts  # Pass posts to template
    }
    return render(request, 'blogsite/profile.html', context)



def user_profile(request, username):
    author = get_object_or_404(User, username=username)
    context = {
        'author': author
    }
    return render(request, 'blogsite/user_profile.html', context)

@login_required
def update_post(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return redirect('user_profile', username=request.user.username)
    else:
        form = PostForm(instance=post)
    return render(request, 'blogsite/update_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect('user_profile', username=request.user.username)
    return render(request, 'blogsite/delete_post.html', {'post': post})
