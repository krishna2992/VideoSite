from rest_framework import serializers
from app.models import Channel, Item, Comment, Unattended, Tag, Actor, Resolution_Video
from django.contrib.auth.models import User
from json import dumps

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id','name', 'views','profile_picture','subscribers_count']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name',]

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['name',]

class ItemChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['name', 'subscribers_count', ]


class ChannelNameSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['name', ]


class ItemPreviewSerializer(serializers.ModelSerializer):
    channel = ChannelNameSerizlizer()
    isFull = serializers.SerializerMethodField()
    class Meta:
        model = Item
        fields = ['name', 'uuid', 'views', 'duration', 'channel', 'profile_picture', 'thumb', 'isFull',]
    def get_isFull(self, obj):
        # Custom method to convert Python boolean to JSON boolean
        return dumps(obj.isFull)  # This will output 'true' or 'false' in JSON


class ItemResolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resolution_Video
        fields = ['resolution', 'video',]


class ItemSerializer(serializers.ModelSerializer):
    channel = ItemChannelSerializer()
    tags = TagSerializer(many=True)
    actors = ActorSerializer(many=True)
    isFull = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    resolutions = ItemResolutionSerializer(many=True)
    class Meta:
        model = Item
        fields = ['id', 'name', 'uuid', 'views', 'tags','actors', 'duration', 'isFull','channel','thumb','profile_picture','comment_count', 'resolutions', ]

    def get_isFull(self, obj):
        # Custom method to convert Python boolean to JSON boolean
        return dumps(obj.isFull)  # This will output 'true' or 'false' in JSON
    
    def get_comment_count(self, obj):
        return obj.comments.count()
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username',]

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Serializer for ForeignKey field to User
    class Meta:
        model = Comment
        fields = ['content', 'user',]


class UnattendedSerializer(serializers.ModelSerializer):
    channel = ItemChannelSerializer()
    class Meta:
        model = Unattended
        fields = ['name', 'isFull','channel','duration', 'profile_picture']