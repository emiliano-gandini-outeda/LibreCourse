from fastapi import HTTPException, Request
from typing import Dict
import time
from collections import defaultdict, deque

class RateLimiter:
    def __init__(self, max_requests: int = 5, window_seconds: int = 300):  # 5 requests per 5 minutes
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, deque] = defaultdict(deque)
    
    def is_allowed(self, identifier: str) -> bool:
        now = time.time()
        window_start = now - self.window_seconds
        
        # Clean old requests
        while self.requests[identifier] and self.requests[identifier][0] < window_start:
            self.requests[identifier].popleft()
        
        # Check if under limit
        if len(self.requests[identifier]) < self.max_requests:
            self.requests[identifier].append(now)
            return True
        
        return False
    
    def __call__(self, request: Request):
        # Use IP address as identifier
        client_ip = request.client.host
        
        if not self.is_allowed(client_ip):
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later."
            )

# Create rate limiter instances
login_rate_limiter = RateLimiter(max_requests=5, window_seconds=300)  # 5 login attempts per 5 minutes
