import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "DEV_KEY"  # CSRF token
