import requests
import jwt
from jwt import PyJWKClient
from flask import Flask, request, jsonify

# Apple's public key URL
APPLE_PUBLIC_KEY_URL = "https://appleid.apple.com/auth/keys"
APPLE_ISSUER = "https://appleid.apple.com"
APPLE_AUD = "com.ianargyle.SwiftUI-Boilerplate"  # Replace with your app's bundle ID


# Fetch Apple's public keys
def get_apple_public_key(kid):
    response = requests.get(APPLE_PUBLIC_KEY_URL)
    jwks = response.json()
    for key in jwks['keys']:
        if key['kid'] == kid:
            return key
    return None


# Validate the JWT from Apple
def validate_apple_jwt(identity_token):
    # Decode JWT headers to get the key ID (kid)
    headers = jwt.get_unverified_header(identity_token)
    kid = headers['kid']

    # Get the corresponding public key from Apple
    public_key_data = get_apple_public_key(kid)
    if not public_key_data:
        return False, "Public key not found"

    # Convert public key data to PEM format
    jwk_client = PyJWKClient(APPLE_PUBLIC_KEY_URL)
    signing_key = jwk_client.get_signing_key_from_jwt(identity_token)

    try:
        # Decode and verify the token
        decoded_token = jwt.decode(
            identity_token,
            signing_key.key,
            algorithms=["RS256"],
            audience=APPLE_AUD,
            issuer=APPLE_ISSUER
        )
        return True, decoded_token
    except jwt.ExpiredSignatureError:
        return False, "Token has expired"
    except jwt.InvalidTokenError:
        return False, "Invalid token"