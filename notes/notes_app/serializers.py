# notes/serializers.py

from rest_framework import serializers
from .models import Note
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class NoteSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Note
        fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'owner')
        read_only_fields = ('id', 'created_at', 'updated_at', 'owner')
