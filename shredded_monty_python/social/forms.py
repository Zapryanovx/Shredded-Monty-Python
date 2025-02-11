from django import forms


class PostForm(forms.Form):
    """
    Form for creating a new post.
    """
    
    text = forms.CharField(
        label="What's on your mind?",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': "Write something...",
            'rows': 3
        }),
        required=False
    )
    image = forms.ImageField(
        label="Upload Image",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    video = forms.FileField(
        label="Upload Video",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )


class CommentForm(forms.Form):
    """
    Form for submitting a comment.
    """
    
    text = forms.CharField(
        label="Write a comment...",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': "Reply to this thread...",
            'rows': 2
        }),
        required=True
    )
