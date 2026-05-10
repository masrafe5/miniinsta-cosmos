from django import forms
from .models import Photo, Comment, Rating
from django.core.exceptions import ValidationError


class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'image', 'caption', 'location', 'people_present', 'tags']
        widgets = {
            'caption': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a caption...'}),
            'location': forms.TextInput(attrs={'placeholder': 'Add a location...'}),
            'people_present': forms.TextInput(attrs={'placeholder': 'Alice, Bob, Charlie...'}),
            'tags': forms.TextInput(attrs={'placeholder': 'travel, food, nature...'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Image file size must be 5MB or smaller.')
            if not image.content_type in ['image/jpeg', 'image/png', 'image/webp']:
                raise ValidationError('Supported image formats: JPEG, PNG, WEBP.')
        return image


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {'text': forms.TextInput(attrs={'placeholder': 'Add a comment...'})}
        labels = {'text': ''}


class RatingForm(forms.ModelForm):
    score = forms.ChoiceField(
        choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)],
        widget=forms.RadioSelect,
        label='Your Rating',
    )

    class Meta:
        model = Rating
        fields = ['score']


class PhotoSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search photos, tags, locations...',
            'class': 'form-control',
        })
    )
