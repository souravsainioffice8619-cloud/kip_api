from fastapi import Request


def get_device_info(request: Request) -> dict:
    """Extract request/device info into a reusable dict."""
    remote_addr = request.client.host if request.client else None
    ip = request.headers.get("X-Forwarded-For", remote_addr)
    user_agent = request.headers.get("User-Agent")

    info = {
        "ip": ip,
        "remote_addr": remote_addr,
        "user_agent": user_agent,
        "browser": None,
        "platform": None,
        "version": None,
        "language": request.headers.get("Accept-Language"),
        "headers": {
            "User-Agent": request.headers.get("User-Agent"),
            "Accept-Language": request.headers.get("Accept-Language"),
            "Referer": request.headers.get("Referer"),
            "X-Forwarded-For": request.headers.get("X-Forwarded-For"),
        },
        "url": str(request.url),
        "method": request.method,
    }

    return info
