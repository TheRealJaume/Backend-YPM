from django.db import transaction

from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from payments.coins.models import UserCoin
from payments.payments.models import UserPayments
from payments.payments.responses import UserPaymentsResponses
from payments.payments.serializers import UserPaymentsSerializer, CreateUserPaymentSerializer, \
    ListUserPaymentSerializer, RetrieveUserPaymentSerializer, UpdateUserPaymentSerializer


class UserPaymentsFilter:
    def filter_queryset(self, request, queryset, view):
        user = request.user
        return queryset.filter(user=user)


class UserPaymentsViewSet(viewsets.ModelViewSet):
    queryset = UserPayments.objects.all()
    lookup_field = 'id'
    serializer_class = UserPaymentsSerializer
    serializer_action_classes = {
        "create": CreateUserPaymentSerializer,
        "list": ListUserPaymentSerializer,
        "retrieve": RetrieveUserPaymentSerializer,
        "update": UpdateUserPaymentSerializer,
    }
    filter_backends = [
        UserPaymentsFilter,
        SearchFilter, OrderingFilter]
    permission_classes = [
        # UserPaymentPermission,
        IsAuthenticated]

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            super().get_serializer_class()

    def retrieve(self, request, *args, **kwargs):
        try:
            user_payment = UserPayments.objects.get(user_id=request.user.id)
            serializer = self.get_serializer(user_payment)
            return Response(UserPaymentsResponses.RetrieveUserPayments200(serializer.data), 200)
        except UserPayments.DoesNotExist:
            return Response(UserPaymentsResponses.RetrieveUserPayments404(error=serializer.errors), 404)

    def update(self, request, *args, **kwargs):
        try:
            payment = UserPayments.objects.filter(transaction_id=kwargs['id'])
            if payment.exists():
                serializer_class = self.get_serializer_class()
                serializer = serializer_class(data=request.data['updated_amount'])
                is_valid = serializer.is_valid()
                if is_valid:
                    serializer.update(instance=payment.first(), validated_data=serializer.validated_data)
                    # Update the total amount of coins
                    user_coins = UserCoin.objects.filter(user=request.user)
                    prev_coins = user_coins.first().coins
                    actual_coins = prev_coins + payment.first().coins
                    user_coins.update(coins=actual_coins)
                    return Response(UserPaymentsResponses.UpdateUserPayments200(
                        {"coins": actual_coins,
                         "payment": UserPaymentsSerializer(payment.first()).data
                         }
                    ),
                        200)
                else:
                    return Response(UserPaymentsResponses.UpdateUserPayments400(error=serializer.errors), 400)
            else:
                return Response(UserPaymentsResponses.UpdateUserPayments404(error="User history payment not found"),
                                404)
        except Exception as e:
            return Response(UserPaymentsResponses.UpdateUserPayments500(error="Error updating user payment"),
                            500)

    def list(self, request, *args, **kwargs):
        # Filtrar el queryset según el filtro configurado
        queryset = self.filter_queryset(self.get_queryset())

        # Si el queryset está vacío, devolver un 204
        if not queryset.exists():
            return Response(UserPaymentsResponses.ListUserPayments204(), 204)

        # Si hay resultados, proceder normalmente
        serializer = self.get_serializer(queryset, many=True)
        return Response(UserPaymentsResponses.ListUserPayments200(serializer.data), 200)

