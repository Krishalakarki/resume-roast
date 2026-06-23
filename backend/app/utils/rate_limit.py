import time
from collections import defaultdict

# store user request timestamps
user_requests = defaultdict(list)

# limit config
MAX_REQUESTS = 5
TIME_WINDOW = 60  # seconds


def is_allowed(user_email: str):

    now = time.time()

    # keep only recent requests
    user_requests[user_email] = [
        t for t in user_requests[user_email]
        if now - t < TIME_WINDOW
    ]

    if len(user_requests[user_email]) >= MAX_REQUESTS:
        return False

    user_requests[user_email].append(now)

    return True