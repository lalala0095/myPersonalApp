from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import os
from flask import flash

MONGO_URI = os.environ.get('MONGO_URI')

def encrypt_card(card_number, password):
    # Generate a random salt
    salt = os.urandom(16)
    print("Generated Salt:", salt)  # Debugging
    
    # Derive a key from the password and salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    print("Derived Key (Encryption):", key)  # Debugging
    
    # Encrypt the card number
    cipher = Fernet(key)
    encrypted_card = cipher.encrypt(card_number.encode())
    print("Encrypted Card:", encrypted_card)  # Debugging
    
    return encrypted_card, salt

def decrypt_card(encrypted_card, salt, password):
    print("Retrieved Salt:", salt)  # Debugging
    
    # Derive a key from the password and salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    print("Derived Key (Decryption):", key)  # Debugging
    
    # Decrypt the card number
    cipher = Fernet(key)
    decrypted_card = cipher.decrypt(encrypted_card)
    return decrypted_card.decode()

from pymongo import MongoClient

def store_encrypted_card(card_id, encrypted_card, salt, category_label):
    mongo = MongoClient(MONGO_URI)
    db = mongo['my_personal']
    collection = db["card_encryptions"]
    
    # Store encrypted data and salt
    collection.insert_one({
        "card_id": card_id,
        "encrypted_card": encrypted_card.decode(),  # Store as string
        "salt": base64.b64encode(salt).decode(), # Encode salt for storage
        "category_label": category_label
    })

def retrieve_encrypted_card():
    mongo = MongoClient(MONGO_URI)
    db = mongo['my_personal']
    collection = db["records"]
    
    # Retrieve stored data
    stored_data = collection.find_one()
    encrypted_card = stored_data["encrypted_card"].encode()  # Decode back to bytes
    salt = base64.b64decode(stored_data["salt"])  # Decode salt back to bytes
    
    return encrypted_card, salt


def encrypt_account_number(card_id, card_number, expiration, cvv, password):
    # Encrypt and store
    # card_number = "4111111111111111"
    # password = "my_secure_password"
    try:
        encrypted_card, salt = encrypt_card(card_number, password)
        store_encrypted_card(card_id, encrypted_card, salt, "account_number")

        encrypted_expiration, salt = encrypt_card(expiration, password)
        store_encrypted_card(card_id, encrypted_expiration, salt, "expiration")

        encrypted_cvv, salt = encrypt_card(cvv, password)
        store_encrypted_card(card_id, encrypted_cvv, salt, "cvv")

        flash("Encrypting encryptions done")
        # Retrieve and decrypt
        # encrypted_card, salt = retrieve_encrypted_card()
        # decrypt_card_number = decrypt_card(encrypted_card, salt, password)
    except Exception as e:
        flash(f"Error occured. Please contact customer support and send this error code: {e}")
    return None

