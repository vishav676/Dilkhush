import secrets
import string

def generate_secret_key(length=50):
    """Generate a secure random secret key."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_password_salt(length=32):
    """Generate a secure random password salt."""
    return secrets.token_hex(length)

if __name__ == '__main__':
    secret_key = generate_secret_key()
    password_salt = generate_password_salt()
    
    print("Generated secure keys:")
    print(f"SECRET_KEY = '{secret_key}'")
    print(f"SECURITY_PASSWORD_SALT = '{password_salt}'")
    
    print("\nCopy these values to your .env file:")
    print(f"FLASK_SECRET_KEY={secret_key}")
    print(f"FLASK_SECURITY_PASSWORD_SALT={password_salt}") 