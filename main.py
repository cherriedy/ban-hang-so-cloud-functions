# main.py
# Cloud Function to retrieve a user's stores from Firestore

from typing import Optional  # Import Optional type hint

from get_user_stores import get_user_stores
from get_user_stores_http import get_user_stores_http

# Global variables for Firebase app and Firestore client
firebase_app: Optional[object] = None  # Will hold the initialized Firebase app

db: Optional[object] = None  # Will hold the Firestore client

# Export all functions for Firebase discovery
get_user_stores_fn = get_user_stores
get_user_stores_http_fn = get_user_stores_http
