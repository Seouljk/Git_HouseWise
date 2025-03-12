# housewise/utils.py

from rest_framework_simplejwt.tokens import RefreshToken

def generate_token(user):
    """
    Generate JWT tokens for a given user.
    Returns a dictionary containing the access and refresh tokens.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
