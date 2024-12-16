import stripe
import uuid

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings

from payments.payments.models import UserPayments
from payments.responses import StripeResponses
from ypm.settings.base import CLIENT_URL


class StripeViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            super().get_serializer_class()

    @action(detail=False, methods=["post"])
    def checkout_session(self, request):
        """
        Endpoint para crear una sesión de Stripe Checkout.
        """
        try:
            # Leer la cantidad enviada desde el frontend
            coins = request.data.get("coins", 0)
            price = request.data.get("price", 0)

            if (not price or price <= 0) or (not coins or coins <= 0):
                return Response(StripeResponses.CheckoutSession400(), 400)
            # Set Stripe secret key
            stripe.api_key = settings.STRIPE_SECRET_KEY

            # Generate a unique session ID for this checkout session
            session_id = str(uuid.uuid4())

            # Crear la sesión de Stripe Checkout
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "eur",
                            "product_data": {
                                "name": f"{coins} Coins",
                            },
                            "unit_amount": price * 100,  # Convert euros into cents
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=CLIENT_URL + f"/coins?payment=success&id={session_id}",
                cancel_url=CLIENT_URL + f"/coins?payment=cancel&id={session_id}",
            )

            # Create a new User Payment history entry
            user_payment = UserPayments(user=request.user, amount=price, coins=coins,
                                        transaction_id=session_id, status=UserPayments.STATUS_PENDING)
            user_payment.save()
            return Response(StripeResponses.CheckoutSession200({"url": session.url, "session_id": session_id}), 200)
        except stripe.error.StripeError as e:
            return Response(StripeResponses.CheckoutSession500(error=str(e)), 500)
        except Exception as e:
            return Response(StripeResponses.CheckoutSession500(error="An unexpected error occurred."), 500)