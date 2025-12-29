import bcrypt
from datetime import datetime
from .db import get_db_connection


# ---------------------------------------------------------
# HASH PASSWORD (bcrypt)
# ---------------------------------------------------------
def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


# ---------------------------------------------------------
# VERIFY PASSWORD
# ---------------------------------------------------------
def verify_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)


# ---------------------------------------------------------
# SIGNUP USER
# ---------------------------------------------------------
def signup_user(name: str, email: str, password: str):
    conn = get_db_connection()
    cur = conn.cursor()

    # Check if email already exists
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    existing_user = cur.fetchone()

    if existing_user:
        return False, "Email already exists. Try logging in."

    # Create hashed password
    hashed_pw = hash_password(password)

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insert into database
    cur.execute("""
        INSERT INTO users (name, email, password_hash, created_at)
        VALUES (?, ?, ?, ?)
    """, (name, email, hashed_pw, created_at))

    conn.commit()
    conn.close()

    return True, "Signup successful! You can now log in."


# ---------------------------------------------------------
# LOGIN USER
# ---------------------------------------------------------
def login_user(email: str, password: str):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cur.fetchone()

    if not user:
        return False, "No account found with this email."

    stored_hash = user["password_hash"]

    if not verify_password(password, stored_hash):
        return False, "Incorrect password."

    return True, user


# ---------------------------------------------------------
# GET USER BY ID
# ---------------------------------------------------------
def get_user_by_id(user_id: int):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()

    return user


# ---------------------------------------------------------
# CHANGE PASSWORD
# ---------------------------------------------------------
def change_password(user_id: int, old_password: str, new_password: str):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()

    if not user:
        return False, "User not found."

    stored_hash = user["password_hash"]

    # Verify old password
    if not verify_password(old_password, stored_hash):
        return False, "Old password is incorrect."

    # Hash new password
    new_hash = hash_password(new_password)

    # Update in database
    cur.execute("""
        UPDATE users SET password_hash = ?
        WHERE id = ?
    """, (new_hash, user_id))

    conn.commit()
    conn.close()

    return True, "Password changed successfully!"


# ---------------------------------------------------------
# UPDATE USER NAME (OPTIONAL)
# ---------------------------------------------------------
def update_user_name(user_id: int, new_name: str):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE users SET name = ?
        WHERE id = ?
    """, (new_name, user_id))

    conn.commit()
    conn.close()

    return True, "Name updated successfully!"
