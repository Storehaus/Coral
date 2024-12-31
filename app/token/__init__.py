from datetime import datetime, timedelta
from threading import Lock, Timer
import uuid
from config import app_config

TOKEN_EXPIRY_TIME = int(app_config.get("TOKEN_EXPIRY_TIME", "30"))  # seconds

class TokenManager:
  def __init__(self):
    self.token_cache = {}
    self.cache_lock = Lock()

  def remove_expired_token(self, token):
    """Remove the token from the cache after expiration"""
    with self.cache_lock:
      if token in self.token_cache:
        del self.token_cache[token]
        
  def check_if_token_exists(self, token):
    with self.cache_lock:
      if token in self.token_cache:
        return True
      else:
        return False

  def create_new_token(self):
    token = str(uuid.uuid4())
    expiration_time = datetime.utcnow() + timedelta(seconds=TOKEN_EXPIRY_TIME)

    with self.cache_lock:
      self.token_cache[token] = expiration_time

    # Schedule a token for removal
    Timer(TOKEN_EXPIRY_TIME, self.remove_expired_token, args=[token]).start()
    return token
