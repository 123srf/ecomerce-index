from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        initial=5,
        widget=forms.HiddenInput(attrs={'id': 'ratingInput'})
    )

    class Meta:
        model = Review
        fields = ['rating', 'name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'reviewName',
                'placeholder': 'Your Name',
                'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'reviewEmail',
                'placeholder': 'Your Email',
                'required': 'required'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'reviewMessage',
                'rows': 5,
                'placeholder': 'Your Review',
                'required': 'required'
            }),
        }

