from django import forms
from multiupload.fields import MultiFileField
from .models import Comments, add_product, Profile
from django.contrib.auth.models import User

class add_product_product(forms.ModelForm):
    images = MultiFileField(max_length=200, allow_empty_file=True, required=False)

    class Meta:
        model = add_product
        fields = ['name', 'price', 'description', 'images']

class NewCommentForm(forms.ModelForm):
    class Meta: 
        model = Comments
        fields = '__all__'

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']