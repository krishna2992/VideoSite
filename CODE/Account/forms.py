from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from app.models import Channel

class SignupForm(forms.Form):
    name = forms.CharField(label='Channel Name', max_length=100)
    username = forms.CharField(label='Username', max_length=50)
    email = forms.EmailField(label='Email',required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password1 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    profile_picture = forms.ImageField(label='Profile Picture', required=False)
    description = forms.CharField(
        label='Enter your text',
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter Appropriate Description of Your Channel in 250 Characters',
            'rows': 4,  # Number of visible text lines
            # 'cols': 64,  # Width of the textarea
            'class':'description',
        }),
        max_length=250,
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Channel.objects.filter(name=name).exists():
            raise forms.ValidationError("Name is already taken.")

        return name



    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Example: Check if username already exists in the database
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken.")

        # You can add more specific validation rules for username here

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Example: Check if email is already registered
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already registered.")

        

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password1 = cleaned_data.get('password1')

        if password and password1 and password != password1:
            raise forms.ValidationError("Passwords do not match.")


    def save(self):
        name = self.cleaned_data['name']
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        profile_picture = self.cleaned_data['profile_picture']
        
        user = User.objects.create_user(username=username, email=email, password=make_password(password))
        channel = Channel.objects.create(name=name, user=user, profile_picture=profile_picture, type='channel')
        return channel
        

class UserSignupForm(forms.Form):
    
    username = forms.CharField(label='Username', max_length=50)
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password1 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Example: Check if username already exists in the database
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken.")

        # You can add more specific validation rules for username here

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Example: Check if email is already registered
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already registered.")

        # You can add more specific validation rules for email here

        return email


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password1 = cleaned_data.get('password1')

        if password and password1 and password != password1:
            raise forms.ValidationError("Passwords do not match.")
    

    def save(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        user = User.objects.create_user(username=username, email=email, password=make_password(password))
        return user




class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ['name', 'type', 'user', 'profile_picture']