from flask import Request


def get_device_info(request: Request) -> dict:
    """Extract device/request info into a dict (for reuse across controllers)."""
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = request.user_agent  # provides .string, .browser, .platform, .version

    info = {
        "ip": ip,
        "remote_addr": request.remote_addr,
        "user_agent": user_agent.string,
        "browser": user_agent.browser,
        "platform": user_agent.platform,
        "version": user_agent.version,
        "language": request.headers.get("Accept-Language"),
        "headers": {
            "User-Agent": request.headers.get("User-Agent"),
            "Accept-Language": request.headers.get("Accept-Language"),
            "Referer": request.headers.get("Referer"),
            "X-Forwarded-For": request.headers.get("X-Forwarded-For"),
        },
        "url": request.url,
        "method": request.method,
    }

    return info
