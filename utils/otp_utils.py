import random
from datetime import datetime, timedelta, timezone

def generate_otp() -> str:
    """Generate a 6-digit random numeric OTP."""
    return str(random.randint(100000, 999999))

def otp_expiry_time(minutes: int = 5):
    """Return an expiry timestamp for OTP."""
    return datetime.now(timezone.utc) + timedelta(minutes=minutes)
