from werkzeug.security import generate_password_hash, check_password_hash

# Hash a password for secure storage
def hash_password(password):
    return generate_password_hash(password)

# Check if the provided password matches the stored hash
def verify_password(hashed_password, password):
    return check_password_hash(hashed_password, password)
