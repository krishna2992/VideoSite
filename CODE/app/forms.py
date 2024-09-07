# myapp/forms.py
from django import forms
from .models import Item, Actor, Tag, Unattended
import re
# from django.contrib.admin.widgets import FilteredSelectMultiple


class UnattendedFormMain(forms.ModelForm):
    class Meta:
        model = Unattended
        fields = ['name', 'actors', 'tags', 'isFull', 'video',]





# class UnattendedForm(forms.ModelForm):
#     class Meta:
#         model = Unattended
#         fields = ['name', 'filter_actors', 'actors', 'filter_tags', 'tags', 'isFull', 'video',]

#     actors = forms.ModelMultipleChoiceField(
#         queryset=Actor.objects.all(),
#         widget=forms.SelectMultiple(attrs={'class': 'actors-select'})
#     )

#     tags = forms.ModelMultipleChoiceField(
#         queryset=Tag.objects.all(),
#         widget=forms.SelectMultiple(attrs={'class': 'tags-select'})
#     )

#     filter_actors = forms.CharField(
#         required=False,
#         label='Filter Actors',
#         widget=forms.TextInput(attrs={'class': 'filter-input', 'placeholder': 'Filter actors...', 'id':'filterActors'})
#     )

#     filter_tags = forms.CharField(
#         required=False,
#         label='Filter Tags',
#         widget=forms.TextInput(attrs={'class': 'filter-input', 'placeholder': 'Filter tags...', 'id':'filterTags'})
#     )

#     # video = forms.FileField(
#     #     label='Video Upload',  # Label for the field
#     #     required=True,  # Set to True if video upload is mandatory
#     #     widget=forms.ClearableFileInput(attrs={'accept': 'video/*'})  # Accept only video files
#     # )

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['actors'].widget.attrs.update({'class': 'actors-select'})
#         self.fields['tags'].widget.attrs.update({'class': 'tags-select'})

from django import forms
from .models import Unattended, Actor, Tag

class UnattendedForm(forms.ModelForm):
    class Meta:
        model = Unattended
        fields = ['name', 'filter_actors', 'actors', 'filter_tags', 'tags', 'isFull', 'video']

    actors = forms.ModelMultipleChoiceField(
        queryset=Actor.objects.all().values_list('name', flat=True),
        widget=forms.SelectMultiple(attrs={'class': 'actors-select'})
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all().values_list('name', flat=True),
        widget=forms.SelectMultiple(attrs={'class': 'tags-select'})
    )

    filter_actors = forms.CharField(
        required=False,
        label='Filter Actors',
        widget=forms.TextInput(attrs={'class': 'filter-input', 'placeholder': 'Filter actors...', 'id': 'filterActors'})
    )

    filter_tags = forms.CharField(
        required=False,
        label='Filter Tags',
        widget=forms.TextInput(attrs={'class': 'filter-input', 'placeholder': 'Filter tags...', 'id': 'filterTags'})
    )

    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Update widget attributes
        self.fields['actors'].widget.attrs.update({'class': 'actors-select'})
        self.fields['tags'].widget.attrs.update({'class': 'tags-select'})
        self.fields['video'].widget.attrs.update({'accept': 'video/*'})
        

    def clean_actors(self):
        actors = self.cleaned_data.get('actors')
        # Ensure at least one actor is selected
        if not actors:
            raise forms.ValidationError("Please select at least one actor.")
        return actors
    
    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        cleaned_tags = []

        # Loop through selected tags and create if not exists
        for tag_name in tags:
            tag_obj, created = Tag.objects.get_or_create(name=tag_name)
            cleaned_tags.append(tag_obj)

        return cleaned_tags
    
    

    def save(self, commit=True):
        instance = super().save(commit=False)
        print()
        if commit:
            instance.save()

        # Process input_tags and create tags if necessary
        
        tags_list = self.clean_tag()
        actors_list = self.clean_actors()

        

        for tag_name in tags_list:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            instance.tags.add(tag)

        for actor_name in actors_list:
            actor, created = Actor.objects.get_or_create(name=actor_name)
            instance.actors.add(actor)
    
        return instance
    



class UnattendedFormNew(forms.Form):
    name = forms.CharField(max_length=100)

    actors = forms.ModelMultipleChoiceField(
        queryset=Actor.objects.all().values_list('name', flat=True),
        widget=forms.SelectMultiple(attrs={'class': 'actors-select'})
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all().values_list('name', flat=True),
        widget=forms.SelectMultiple(attrs={'class': 'tags-select'})
    )

    filter_actors = forms.CharField(
        required=False,
        label='Filter Actors',
        widget=forms.TextInput(attrs={'class': 'filter-input', 'placeholder': 'Filter actors...', 'id': 'filterActors'})
    )

    filter_tags = forms.CharField(
        required=False,
        label='Filter Tags',
        widget=forms.TextInput(attrs={'class': 'filter-input', 'placeholder': 'Filter tags...', 'id': 'filterTags'})
    )

    video = forms.FileField(
        required=False,
        label='Filter Tags',
    )
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Update widget attributes
        self.fields['actors'].widget.attrs.update({'class': 'actors-select'})
        self.fields['tags'].widget.attrs.update({'class': 'tags-select'})
        self.fields['video'].widget.attrs.update({'accept': 'video/*'})
        

    def clean_actors(self):
        actors = self.cleaned_data.get('actors')
        # Ensure at least one actor is selected
        if not actors:
            raise forms.ValidationError("Please select at least one actor.")
        return actors
    
    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        cleaned_tags = []

        # Loop through selected tags and create if not exists
        for tag_name in tags:
            tag_obj, created = Tag.objects.get_or_create(name=tag_name)
            cleaned_tags.append(tag_obj)

        return cleaned_tags
    
    

    
class VideoForm(forms.Form):
    name = forms.CharField(max_length=100)
    actors = forms.CharField(required=True)
    filter_actors = forms.CharField(required=False)
    actors_select = forms.ChoiceField(choices=[], widget=forms.Select, required=False)
    tags = forms.CharField(required=True)
    filter_tags = forms.CharField(required=False)
    tags_select = forms.ChoiceField(choices=[], widget=forms.Select, required=False)
    isFull = forms.BooleanField(required=False)
    profile = forms.ImageField(label='Upload a Thumb Image for Video', required=False, help_text='Max. 500KB')
    video = forms.FileField(label='Select a video file', help_text='Max. 20MB')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Update widget attributes
        self.fields['actors'].widget.attrs.update({'class': 'actors-select form-control'})
        self.fields['tags'].widget.attrs.update({'class': 'tags-select form-control'})
        self.fields['video'].widget.attrs.update({'accept': 'video/*'})
        self.fields['actors_select'].choices = [('', 'Select an actor')] +[(actor.name, actor.name) for actor in Actor.objects.all()]
        self.fields['tags_select'].choices = [('', 'Select a tags')] +[(tag.name, tag.name) for tag in Tag.objects.all()]
    


class MetaDataForm(forms.Form):
    name = forms.CharField(max_length=100)
    actors = forms.CharField(required=True)
    filter_actors = forms.CharField(required=False)
    actors_select = forms.ChoiceField(choices=[], widget=forms.Select, required=False)
    tags = forms.CharField(required=True)
    filter_tags = forms.CharField(required=False)
    tags_select = forms.ChoiceField(choices=[], widget=forms.Select, required=False)
    isFull = forms.BooleanField(required=False)
    video = forms.FileField(label='Select a video file',  required=False)
    profile = forms.ImageField(label='Upload a Thumb Image for Video', required=False, help_text='Max. 500KB')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Update widget attributes
        self.fields['actors'].widget.attrs.update({'class': 'actors-select form-control'})
        self.fields['tags'].widget.attrs.update({'class': 'tags-select form-control'})
        self.fields['video'].widget.attrs.update({'accept': 'video/*'})
        self.fields['actors_select'].choices = [('', 'Select an actor')] +[(actor.name, actor.name) for actor in Actor.objects.all()]
        self.fields['tags_select'].choices = [('', 'Select a tags')] +[(tag.name, tag.name) for tag in Tag.objects.all()]
    

    

    def save(self, channel, commit=True):
        # Get cleaned data from the form
        name = re.sub('\s+', ' ', self.cleaned_data['name'])
        is_full = self.cleaned_data['isFull']
        profile = self.cleaned_data['profile']
        
        
        metadata_instance = Unattended(
            name=name,
            isFull=is_full,
            profile_picture=profile,
            channel=channel
        )

        metadata_instance.save()
        actor_names = self.cleaned_data['actors'].split(',')
        tag_names = self.cleaned_data['tags'].split(',')

        # Get or create Actor and Tag instances
        for actor_name in actor_names:
            if not actor_name:
                continue
            actor_obj, created = Actor.objects.get_or_create(name=actor_name.strip())
            metadata_instance.actors.add(actor_obj)

        for tag_name in tag_names:
            if not tag_name:
                continue
            tag_obj, created = Tag.objects.get_or_create(name=tag_name.strip())
            metadata_instance.tags.add(tag_obj)
        metadata_instance.save()
        return metadata_instance