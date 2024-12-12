from django.db import transaction
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from payments.coins.models import UserCoin
from payments.coins.responses import UserCoinResponses
from payments.coins.serializers import UserCoinsSerializer, CreateUserCoinSerializer, RetrieveUserCoinsSerializer, \
    UpdateUserCoinSerializer


class UserCoinsFilter:

    def filter_queryset(self, queryset):
        user = self.request.user
        return queryset.filter(user=user)


class UserCoinViewSet(viewsets.ModelViewSet):
    queryset = UserCoin.objects.all()
    lookup_field = 'user_id'
    serializer_class = UserCoinsSerializer
    serializer_action_classes = {
        "create": CreateUserCoinSerializer,
        # "list": ListUserCoinsSerializer,
        "retrieve": RetrieveUserCoinsSerializer,
        "update": UpdateUserCoinSerializer
    }
    filter_backends = [
        UserCoinsFilter,
        SearchFilter, OrderingFilter]
    permission_classes = [
        # CompanyUserPermission,
        IsAuthenticated]

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            super().get_serializer_class()

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        user_coin = UserCoin.objects.filter(user__id=kwargs['user_id'])
        if user_coin.exists():
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data)
            is_valid = serializer.is_valid()
            if is_valid:
                serializer.update(instance=user_coin.first(), validated_data=serializer.validated_data)
                return Response(UserCoinResponses.UpdateUserCoin200(),
                                200)
            else:
                return Response(UserCoinResponses.UpdateUserCoin400(error=serializer.errors), 400)
        else:
            return Response(UserCoinResponses.UpdateUserCoin404(error="UserCoins not found"),
                            404)

    def retrieve(self, request, *args, **kwargs):
        try:
            user_coin = UserCoin.objects.get(user_id=request.user.id)
            serializer = self.get_serializer(user_coin)
            return Response(UserCoinResponses.RetrieveUserCoin200(serializer.data), 200)
        except UserCoin.DoesNotExist:
            return Response(UserCoinResponses.RetrieveUserCoin404(error=serializer.errors), 404)