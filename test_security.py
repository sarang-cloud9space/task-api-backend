
from security import hash_password, verify_password

# Original password (only for this local test)
password = "TestPassword123!"

# Hash the password
hashed = hash_password(password)

print("Original password:", password)
print("Hashed password:", hashed)
print("Hash is different from password:", hashed != password)

# Verify correct and incorrect passwords
print("Correct password accepted:", verify_password(password, hashed))
print("Wrong password accepted:", verify_password("WrongPassword", hashed))
