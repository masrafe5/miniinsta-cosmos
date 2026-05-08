from django import forms
from .models import Photo, Comment, Rating


class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model   = Photo
        fields  = ['title', 'image', 'caption', 'location', 'people_present', 'tags']
        widgets = {
            'caption':        forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a caption...'}),
            'location':       forms.TextInput(attrs={'placeholder': 'Add a location...'}),
            'people_present': forms.TextInput(attrs={'placeholder': 'Alice, Bob, Charlie...'}),
            'tags':           forms.TextInput(attrs={'placeholder': 'travel, food, nature...'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model   = Comment
        fields  = ['text']
        widgets = {'text': forms.TextInput(attrs={'placeholder': 'Add a comment...'})}
        labels  = {'text': ''}


class RatingForm(forms.ModelForm):
    score = forms.ChoiceField(
        choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)],
        widget=forms.RadioSelect,
        label='Your Rating',
    )

    class Meta:
        model  = Rating
        fields = ['score']


class PhotoSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search photos, tags, locations...',
            'class': 'form-control',
        })
    )
