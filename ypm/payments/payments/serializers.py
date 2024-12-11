from rest_framework import serializers

from payments.payments.models import UserPayments


# GENERIC
class UserPaymentsSerializer(serializers.ModelSerializer):
    """ Serializer for UserPayments basic information"""
    id = serializers.CharField(source='transaction_id')
    date = serializers.CharField(source='modified')

    class Meta:
        model = UserPayments
        fields = ('amount', 'coins', 'id', 'date', 'status')


# CREATE
class CreateUserPaymentSerializer(serializers.ModelSerializer):
    """ Serializer for create user payment registration"""

    class Meta:
        model = UserPayments
        fields = ('amount', 'coins', 'transaction_id', 'user')


# LIST
class ListUserPaymentSerializer(serializers.ModelSerializer):
    """ Serializer for list user payment history"""

    id = serializers.CharField(source='transaction_id')
    date = serializers.CharField(source='modified')

    class Meta:
        model = UserPayments
        fields = ('amount', 'coins', 'id', 'status', 'date')


# RETRIEVE
class RetrieveUserPaymentSerializer(serializers.ModelSerializer):
    """ Serializer for retrieve user payment history"""

    class Meta:
        model = UserPayments
        fields = ('id', 'amount', 'coins', 'transaction_id')


# UPDATE
class UpdateUserPaymentSerializer(serializers.ModelSerializer):
    """ Serializer for updating user payment history"""

    class Meta:
        model = UserPayments
        fields = ('status',)
