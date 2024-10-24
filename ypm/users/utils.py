# Store the tokens in the user request session
def store_tokens_in_session(request, access_token, refresh_token):
    request.session['access_token'] = access_token
    request.session['refresh_token'] = refresh_token
    # Guarda explícitamente la sesión
    request.session.save()
    return "Tokens almacenados en la sesión con éxito."


# Retrieve tokens from the session
def get_tokens_from_session(request):
    access_token = request.session.get('access_token', None)
    refresh_token = request.session.get('refresh_token', None)
    if access_token and refresh_token:
        return access_token, refresh_token
    else:
        return "No hay tokens almacenados en la sesión."


# Remove tokens from the user's session
def remove_tokens_from_session(request):
    try:
        del request.session['access_token']
        del request.session['refresh_token']
        request.session.save()
        return "Tokens eliminados de la sesión."
    except KeyError:
        return "No se encontraron tokens en la sesión."
