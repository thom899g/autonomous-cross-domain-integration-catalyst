"""
Firebase Firestore handler for state management and real-time data.
Implements robust error handling, connection pooling, and automatic retries.
"""
import json
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import hashlib
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import Client as FirestoreClient
from google.cloud.firestore_v1 import DocumentSnapshot
from google.cloud.exceptions import GoogleCloudError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import logging

from config import settings, logger

class FirebaseHandler:
    """
    Singleton handler for Firebase Firestore operations.
    Manages connections, implements automatic retries, and ensures data consistency.
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseHandler, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self