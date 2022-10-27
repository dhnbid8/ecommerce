from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User




class ProfileSerializers(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            'id',
            # 'user',
            'name',
            'phonenumber',
            'address',
            'zipcode',
            'get_profile',
        )