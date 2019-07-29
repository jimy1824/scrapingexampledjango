
from rest_framework import serializers

class TweetListSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=200)
    message = serializers.CharField(max_length=200)

