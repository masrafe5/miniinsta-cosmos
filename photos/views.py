from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.views.decorators.http import require_POST

from mongo import db

from users.decorators import creator_required, consumer_required
from .models import (
    Photo,
    Comment,
    Rating,
    Like,
    SavedPhoto
)

from .forms import (
    PhotoUploadForm,
    CommentForm,
    RatingForm,
    PhotoSearchForm
)


def feed(request):

    search_form = PhotoSearchForm(request.GET)

    photos = Photo.objects.select_related(
        'author'
    ).prefetch_related(
        'comments__author',
        'likes',
        'ratings'
    )

    if search_form.is_valid():

        q = search_form.cleaned_data.get('q')

        if q:

            photos = photos.filter(
                Q(title__icontains=q) |
                Q(caption__icontains=q) |
                Q(tags__icontains=q) |
                Q(location__icontains=q) |
                Q(people_present__icontains=q) |
                Q(author__username__icontains=q)
            )

    photos = photos.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True),
    ).order_by('-created_at')

    paginator = Paginator(photos, 9)

    page_obj = paginator.get_page(
        request.GET.get('page')
    )

    trending = Photo.objects.select_related(
        'author'
    ).annotate(
        like_count=Count('likes')
    ).order_by(
        '-like_count',
        '-created_at'
    )[:4]

    recent = Photo.objects.select_related(
        'author'
    ).order_by('-created_at')[:6]

    liked_ids = set()

    if request.user.is_authenticated:

        liked_ids = set(
            Like.objects.filter(
                user=request.user
            ).values_list(
                'photo_id',
                flat=True
            )
        )

    return render(request, 'photos/feed.html', {
        'photos': page_obj,
        'search_form': search_form,
        'liked_ids': liked_ids,
        'comment_form': CommentForm(),
        'trending': trending,
        'recent': recent,
    })


@login_required
@creator_required
def upload_photo(request):

    if request.method == 'POST':

        form = PhotoUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            photo = form.save(commit=False)

            photo.author = request.user

            photo.save()

            # SAVE FULL PHOTO DATA TO COSMOS DB
            db.photos.insert_one({
                'photo_id': photo.id,
                'title': photo.title,
                'caption': photo.caption,
                'tags': photo.tags,
                'location': photo.location,
                'people_present': photo.people_present,
                'author_username': request.user.username,
                'author_email': request.user.email,
                'image': str(photo.image),
                'created_at': str(photo.created_at),
            })

            messages.success(
                request,
                'Photo uploaded!'
            )

            return redirect(
                'photo_detail',
                pk=photo.pk
            )

    else:
        form = PhotoUploadForm()

    return render(
        request,
        'photos/upload.html',
        {'form': form}
    )


def photo_detail(request, pk):

    photo = get_object_or_404(
        Photo,
        pk=pk
    )

    comments = photo.comments.select_related(
        'author'
    )

    user_rating = None
    user_liked = False
    user_saved = False

    if request.user.is_authenticated:

        user_rating = Rating.objects.filter(
            photo=photo,
            user=request.user
        ).first()

        user_liked = Like.objects.filter(
            photo=photo,
            user=request.user
        ).exists()

        user_saved = SavedPhoto.objects.filter(
            photo=photo,
            user=request.user
        ).exists()

    return render(request, 'photos/photo_detail.html', {
        'photo': photo,
        'comments': comments,
        'comment_form': CommentForm(),
        'rating_form': RatingForm(),
        'user_rating': user_rating,
        'user_liked': user_liked,
        'user_saved': user_saved,
        'avg_rating': photo.average_rating(),
        'rating_count': photo.rating_count(),
        'likes_count': photo.likes.count(),
    })


@login_required
@require_POST
def add_comment(request, pk):

    photo = get_object_or_404(
        Photo,
        pk=pk
    )

    form = CommentForm(request.POST)

    if form.is_valid():

        comment = form.save(commit=False)

        comment.photo = photo
        comment.author = request.user

        comment.save()

        messages.success(
            request,
            'Comment added!'
        )

    return redirect(
        'photo_detail',
        pk=pk
    )


@login_required
@require_POST
def rate_photo(request, pk):

    photo = get_object_or_404(
        Photo,
        pk=pk
    )

    if photo.author == request.user:

        messages.error(
            request,
            "You can't rate your own photo."
        )

        return redirect(
            'photo_detail',
            pk=pk
        )

    form = RatingForm(request.POST)

    if form.is_valid():

        score = int(
            form.cleaned_data['score']
        )

        _, created = Rating.objects.update_or_create(
            photo=photo,
            user=request.user,
            defaults={'score': score},
        )

        messages.success(
            request,
            f'{"Rated" if created else "Updated rating to"} {score}/5!'
        )

    return redirect(
        'photo_detail',
        pk=pk
    )


@login_required
@require_POST
def like_photo(request, pk):

    photo = get_object_or_404(
        Photo,
        pk=pk
    )

    like, created = Like.objects.get_or_create(
        photo=photo,
        user=request.user
    )

    if not created:
        like.delete()

    return redirect(
        request.POST.get('next', 'feed')
    )


@login_required
@require_POST
def toggle_save_photo(request, pk):

    photo = get_object_or_404(
        Photo,
        pk=pk
    )

    entry, created = SavedPhoto.objects.get_or_create(
        photo=photo,
        user=request.user
    )

    if not created:

        entry.delete()

        messages.info(
            request,
            'Removed from saved photos.'
        )

    else:

        messages.success(
            request,
            'Saved to your collection.'
        )

    next_url = request.POST.get('next')

    if next_url:
        return redirect(next_url)

    return redirect(
        'photo_detail',
        pk=pk
    )


@login_required
@creator_required
def edit_photo(request, pk):

    photo = get_object_or_404(
        Photo,
        pk=pk
    )

    if photo.author != request.user:

        messages.error(
            request,
            'You can only edit your own photos.'
        )

        return redirect(
            'photo_detail',
            pk=pk
        )

    if request.method == 'POST':

        form = PhotoUploadForm(
            request.POST,
            request.FILES,
            instance=photo
        )

        if form.is_valid():

            photo = form.save()

            # UPDATE COSMOS DB
            db.photos.update_one(
                {'photo_id': photo.id},
                {
                    '$set': {
                        'title': photo.title,
                        'caption': photo.caption,
                        'tags': photo.tags,
                        'location': photo.location,
                        'people_present': photo.people_present,
                        'image': str(photo.image),
                    }
                }
            )

            messages.success(
                request,
                'Photo updated!'
            )

            return redirect(
                'photo_detail',
                pk=pk
            )

    else:
        form = PhotoUploadForm(instance=photo)

    return render(request, 'photos/upload.html', {
        'form': form,
        'edit': True,
        'photo': photo
    })


@login_required
@creator_required
@require_POST
def delete_photo(request, pk):

    photo = get_object_or_404(
        Photo,
        pk=pk
    )

    if photo.author != request.user:

        messages.error(
            request,
            'You can only delete your own photos.'
        )

        return redirect(
            'photo_detail',
            pk=pk
        )

    # DELETE FROM COSMOS DB
    db.photos.delete_one({
        'photo_id': photo.id
    })

    photo.delete()

    messages.success(
        request,
        'Photo deleted.'
    )

    return redirect('creator_dashboard')


@login_required
def delete_comment(request, pk):

    comment = get_object_or_404(
        Comment,
        pk=pk
    )

    photo_pk = comment.photo.pk

    if (
        comment.author == request.user
        or
        comment.photo.author == request.user
    ):

        comment.delete()

        messages.success(
            request,
            'Comment deleted.'
        )

    return redirect(
        'photo_detail',
        pk=photo_pk
    )


@login_required
@creator_required
def creator_dashboard(request):

    photos = Photo.objects.filter(
        author=request.user
    ).prefetch_related(
        'comments',
        'likes',
        'ratings'
    )

    total_likes = sum(
        photo.likes.count()
        for photo in photos
    )

    total_comments = sum(
        photo.comments.count()
        for photo in photos
    )

    total_ratings = sum(
        photo.rating_count()
        for photo in photos
    )

    return render(request, 'photos/creator_dashboard.html', {
        'photos': photos,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'total_ratings': total_ratings,
    })


@login_required
@consumer_required
def consumer_dashboard(request):

    saved = SavedPhoto.objects.select_related(
        'photo__author'
    ).filter(
        user=request.user
    )

    trending = Photo.objects.select_related(
        'author'
    ).annotate(
        like_count=Count('likes')
    ).order_by(
        '-like_count',
        '-created_at'
    )[:4]

    recent = Photo.objects.select_related(
        'author'
    ).order_by('-created_at')[:6]

    return render(request, 'photos/consumer_dashboard.html', {
        'saved': saved,
        'trending': trending,
        'recent': recent,
    })