from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from .forms import ConsumerRegistrationForm, CreatorRegistrationForm, ProfileUpdateForm, CustomLoginForm
from .models import CustomUser, Follow
from photos.models import Photo

from mongo import db


def register_consumer(request):
    if request.user.is_authenticated:
        return redirect('feed')

    if request.method == 'POST':
        form = ConsumerRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            # Save user to CosmosDB
            db.users.insert_one({
                "username": user.username,
                "email": user.email,
                "is_creator": False
            })

            login(request, user)

            messages.success(request, f'Welcome to MiniInsta, {user.username}!')

            return redirect('feed')

    else:
        form = ConsumerRegistrationForm()

    return render(request, 'users/register.html', {
        'form': form,
        'title': 'Sign Up'
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed')

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            login(request, user)

            messages.success(request, f'Welcome back, {user.username}!')

            return redirect(request.GET.get('next', 'feed'))

    else:
        form = CustomLoginForm()

    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)

    messages.info(request, 'You have been logged out.')

    return redirect('login')


@login_required
def profile_view(request, username=None):
    profile_user = get_object_or_404(CustomUser, username=username) if username else request.user

    photos = Photo.objects.filter(author=profile_user).order_by('-created_at')

    followers_count = profile_user.followers.count()
    following_count = profile_user.following.count()

    is_following = False

    if request.user != profile_user:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists()

    return render(request, 'users/profile.html', {
        'profile_user': profile_user,
        'photos': photos,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if form.is_valid():
            form.save()

            messages.success(request, 'Profile updated!')

            return redirect('profile')

    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
@require_POST
def follow_user(request, username):
    target = get_object_or_404(CustomUser, username=username)

    if target == request.user:
        messages.error(request, "You can't follow yourself.")

        return redirect('user_profile', username=username)

    obj, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target
    )

    if not created:
        obj.delete()

        messages.info(request, f'Unfollowed {target.username}.')

    else:
        messages.success(request, f'Now following {target.username}!')

    return redirect('user_profile', username=username)


@login_required
def create_creator(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied – staff only.')

        return redirect('feed')

    if request.method == 'POST':
        form = CreatorRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            # Save creator to CosmosDB
            db.users.insert_one({
                "username": user.username,
                "email": user.email,
                "is_creator": True
            })

            messages.success(
                request,
                f'Creator account "{user.username}" created!'
            )

            return redirect('feed')

    else:
        form = CreatorRegistrationForm()

    return render(request, 'users/register.html', {
        'form': form,
        'title': 'Create Creator Account'
    })


@login_required
def explore_users(request):
    users = CustomUser.objects.exclude(
        id=request.user.id
    ).order_by('-date_joined')

    return render(request, 'users/explore_users.html', {
        'users': users
    })