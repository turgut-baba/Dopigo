from rest_framework import serializers
from .models import Store


class StoreSerializer(serializers.ModelSerializer):

    """ I made this in case we need to make a rest api,
        which was my original plan but quickly scrapped."""

    class Meta:
        model = Store
        fields = ["task", "completed", "timestamp", "updated", "user"]