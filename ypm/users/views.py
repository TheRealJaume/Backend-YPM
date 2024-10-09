import json
import requests

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


@csrf_exempt
@api_view(['POST'])
def google_login(request):
    # Get the token from the request body
    body = json.loads(request.body)
    token = body.get('token')

    if not token:
        return Response({'error': 'Token no proporcionado'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Verify the token with Google
        google_token_url = "https://www.googleapis.com/oauth2/v3/tokeninfo"
        response = requests.get(google_token_url, params={'id_token': token})

        if response.status_code != 200:
            return Response({'error': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)

        # Extract user information from Google's response
        user_data = response.json()
        email = user_data.get('email')
        first_name = user_data.get('given_name', '')
        last_name = user_data.get('family_name', '')

        if not email:
            return Response({'error': 'No se pudo obtener el email del token de Google'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if there is already a linked SocialAccount
        try:
            social_account = SocialAccount.objects.get(uid=user_data['sub'], provider='google')
            user = social_account.user

            # If the user exists, log them in
            login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')

            # Generate JWT tokens for the authenticated user
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })

        except SocialAccount.DoesNotExist:
            # User does not exist, create a new user
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Create a new user if it does not exist
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=None  # Users logging in via Google don’t need a password
                )

            # Create a SocialAccount for the new user
            social_account = SocialAccount.objects.create(
                user=user,
                provider='google',
                uid=user_data['sub'],
                extra_data=user_data
            )

            # Link the social account to the user and log them in
            login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')

            # Generate JWT tokens for the authenticated user
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })

    except Exception as e:
        return Response({'error': 'Error al procesar el inicio de sesión con Google', 'details': str(e)},
                        status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def google_logout(request):
    # Method to logout the user from the application
    try:
        refresh_token = request.data['refresh_token']
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response("Logout OK", status=status.HTTP_200_OK)
    except TokenError:
        raise AuthenticationFailed("Invalid Token")


@api_view(['POST'])
def refresh_token(request):
    refresh_token = request.data.get('refresh')

    if not refresh_token:
        return Response({'error': 'Refresh token no proporcionado'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Crea una nueva instancia de RefreshToken a partir del refresh token recibido
        token = RefreshToken(refresh_token)

        # Verifica si el refresh token está expirado
        if token.is_expired():
            return Response({'error': 'Refresh token expirado'}, status=status.HTTP_401_UNAUTHORIZED)

        # Genera un nuevo access token
        access_token = str(token.access_token)

        return Response({'access': access_token}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': 'Error al refrescar el token', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)
