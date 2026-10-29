
import jwt

from auth import create_access_token, decode_access_token

# Create a token for a sample user with ID 1
token = create_access_token(subject="1")

print("Token created:", bool(token))
print("Token has three parts:", len(token.split(".")) == 3)

# Decode and verify the token
payload = decode_access_token(token)

print("User ID from token:", payload["sub"])
print("Token algorithm:", jwt.get_unverified_header(token)["alg"])
print("Token expiration exists:", "exp" in payload)
