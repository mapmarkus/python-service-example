from datetime import timedelta

# Constants used accross the app

# Store key namespace
STORE_KEY = 'session.id.{session_id}'

# Session max age
SESSION_MAX_AGE = timedelta(hours=24)
