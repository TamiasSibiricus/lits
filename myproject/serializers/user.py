from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ..models import UserProfile


class GroupListField(serializers.RelatedField):
    def get_queryset(self):
        return Group.objects.all()

    def to_representation(self, value):
        return value.name

    def to_internal_value(self, data):
        return data


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'id', 'name']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'firstname', 'lastname', 'birth_date']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer()
    password = serializers.CharField(
        max_length=60,
        trim_whitespace=True,
        required=True,
        write_only=True,
        help_text=_(
            "Required. 128 characters or fewer. Letters and digits only."
        )
    )
    email = serializers.EmailField()
    groups = GroupListField(many=True)

    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'password', 'email', 'groups', 'profile']
