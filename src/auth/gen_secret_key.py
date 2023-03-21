import secrets
from werkzeug.security import generate_password_hash


key = secrets.token_urlsafe(64)
print(key)

password_hash = generate_password_hash('ducngonzai')
print(password_hash)