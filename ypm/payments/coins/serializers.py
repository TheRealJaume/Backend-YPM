from rest_framework import serializers
from payments.coins.models import UserCoin


# USER COIN

# GENERIC


class UserCoinsSerializer(serializers.ModelSerializer):
    """ Serializer for UserCoin basic information"""

    class Meta:
        model = UserCoin
        fields = ('id', 'user', 'coins')


# RETRIEVE
class RetrieveUserCoinsSerializer(serializers.ModelSerializer):
    """ Serializer for UserCoin basic information"""

    class Meta:
        model = UserCoin
        fields = ('id', 'user', 'coins')


# CREATE
class CreateUserCoinSerializer(serializers.ModelSerializer):
    """ Serializer for UserCoin create action"""

    class Meta:
        model = UserCoin
        fields = ('user', 'coins')


# UPDATE
class UpdateUserCoinSerializer(serializers.ModelSerializer):
    """ Serializer for UserCoin update action"""

    class Meta:
        model = UserCoin
        fields = 'coins'
